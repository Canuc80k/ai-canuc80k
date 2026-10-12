"""Recipe CUDA tiny, không tải asset. Mặc định chỉ preflight.

python content/phase-3/recipes/gpu_probe.py
python content/phase-3/recipes/gpu_probe.py --run --precision fp32
python content/phase-3/recipes/gpu_probe.py --run --precision amp

Số đo chỉ gồm loop train trên batch đã đặt trên GPU; không gồm đọc/chuyển dữ liệu.
"""
import argparse
import json
import time
import torch
from torch import nn

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', action='store_true')
    parser.add_argument('--precision', choices=['fp32', 'amp'], default='fp32')
    parser.add_argument('--batch', type=int, default=128)
    parser.add_argument('--steps', type=int, default=50)
    parser.add_argument('--warmup', type=int, default=5)
    args = parser.parse_args()
    if min(args.batch, args.steps, args.warmup) <= 0:
        parser.error('batch, steps và warmup phải dương')
    torch.set_num_threads(1)
    torch.manual_seed(31)
    ready = torch.cuda.is_available()
    print(json.dumps({'torch': torch.__version__, 'cuda_build': torch.version.cuda,
        'cuda_available': ready, 'status': 'CUDA_READY' if ready else 'CPU_ONLY'},
        ensure_ascii=False))
    if not args.run:
        print('PREFLIGHT_ONLY: chưa chạy benchmark CUDA')
        return
    if not ready:
        raise SystemExit('CUDA_NOT_AVAILABLE: cần máy CUDA + PyTorch tương thích; không có số đo GPU')
    device = torch.device('cuda')
    x = torch.randn(args.batch, 512, device=device)
    y = torch.randint(0, 10, (args.batch,), device=device)
    model = nn.Sequential(nn.Linear(512, 256), nn.ReLU(), nn.Linear(256, 10)).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    use_amp = args.precision == 'amp'
    scaler = torch.amp.GradScaler('cuda', enabled=use_amp)
    model.train()

    def step():
        optimizer.zero_grad(set_to_none=True)
        with torch.amp.autocast('cuda', dtype=torch.float16, enabled=use_amp):
            loss = nn.functional.cross_entropy(model(x), y)
        scaler.scale(loss).backward()
        scaler.unscale_(optimizer)
        nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        scaler.step(optimizer)
        scaler.update()
        return loss

    try:
        for _ in range(args.warmup):
            step()
        torch.cuda.synchronize()
        torch.cuda.reset_peak_memory_stats()
        start = time.perf_counter()
        for _ in range(args.steps):
            loss = step()
        torch.cuda.synchronize()
        elapsed = time.perf_counter() - start
        if not torch.isfinite(loss).item():
            raise RuntimeError('LOSS_NOT_FINITE: giảm lr, kiểm input và precision')
        print(json.dumps({'device': torch.cuda.get_device_name(), 'precision': args.precision,
            'batch': args.batch, 'warmup': args.warmup, 'steps': args.steps,
            'seconds_train_loop': elapsed, 'milliseconds_per_step': 1000*elapsed/args.steps,
            'samples_per_second': args.batch*args.steps/elapsed,
            'peak_allocated_MiB': torch.cuda.max_memory_allocated()/2**20,
            'peak_reserved_MiB': torch.cuda.max_memory_reserved()/2**20,
            'last_loss': loss.item(), 'includes_data_loading': False}, ensure_ascii=False))
    except torch.cuda.OutOfMemoryError:
        raise SystemExit('CUDA_OOM: giảm --batch rồi chạy lại tiến trình mới; không có benchmark hợp lệ')

if __name__ == '__main__':
    main()
