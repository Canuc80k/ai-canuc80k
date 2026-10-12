# -*- coding: utf-8 -*-
# Code mẫu — Optimizer

# Ví dụ 1: Cùng một gradient, SGD và Adam bước khác nhau
import math
import torch

torch.set_num_threads(1)
w, gradient, lr = 2., -2., .1
beta1, beta2, eps = .9, .999, 1e-8
m = (1 - beta1) * gradient
v = (1 - beta2) * gradient ** 2
m_hat, v_hat = m / (1 - beta1), v / (1 - beta2)
hand_adam = w - lr * m_hat / (math.sqrt(v_hat) + eps)
print("SGD tính tay:", w - lr * gradient)
print("Adam m, v:", round(m, 6), round(v, 6))
print("Adam m_hat, v_hat:", round(m_hat, 6), round(v_hat, 6))

p = torch.nn.Parameter(torch.tensor(w, dtype=torch.float64))
optimizer = torch.optim.Adam([p], lr=lr, betas=(beta1, beta2), eps=eps)
optimizer.zero_grad(set_to_none=True)
(p - 3).square().backward()
optimizer.step()
print("Adam thư viện / tính tay:", round(p.item(), 6), round(hand_adam, 6))
assert math.isclose(p.item(), hand_adam, rel_tol=1e-12)


# Ví dụ 2: Theo dõi từng tọa độ trong một thung lũng hẹp
import torch

torch.set_num_threads(1)
def trajectory(kind, lr):
    p = torch.nn.Parameter(torch.tensor([-2., 1.], dtype=torch.float64))
    if kind == "momentum":
        optimizer = torch.optim.SGD([p], lr=lr, momentum=.8)
    elif kind == "Adam":
        optimizer = torch.optim.Adam([p], lr=lr)
    else:
        optimizer = torch.optim.SGD([p], lr=lr)
    records = []
    for step in range(9):
        loss = p[0].square() + 8 * p[1].square()
        if step in [0, 1, 2, 8]:
            records.append((step, *[round(x, 5) for x in p.detach().tolist()],
                            round(loss.item(), 5)))
        if step < 8:
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()
    return records

for kind, lr in [("SGD", .05), ("momentum", .05), ("Adam", .15), ("SGD", .15)]:
    print(kind, "lr", lr, "(step, w1, w2, loss):", trajectory(kind, lr))


# Ví dụ 3: Gradient bằng 0 khác với chưa có gradient
import torch

torch.set_num_threads(1)
with_zero = torch.nn.Parameter(torch.tensor(2., dtype=torch.float64))
with_none = torch.nn.Parameter(torch.tensor(2., dtype=torch.float64))
optimizer = torch.optim.AdamW([with_zero, with_none], lr=.1, weight_decay=.2)
with_zero.grad = torch.zeros_like(with_zero)
assert with_none.grad is None
optimizer.step()
print("gradient 0:", round(with_zero.item(), 6))
print("gradient None:", round(with_none.item(), 6))
print("tham số có optimizer state:", len(optimizer.state))
assert abs(with_zero.item() - 1.96) < 1e-12 and with_none.item() == 2.


# Ví dụ 4: Muốn học tiếp, phải lưu cả optimizer lẫn scheduler
import copy
import torch

torch.set_num_threads(1)
def make_run(value):
    p = torch.nn.Parameter(torch.tensor(value, dtype=torch.float64))
    opt = torch.optim.Adam([p], lr=.1)
    sched = torch.optim.lr_scheduler.StepLR(opt, step_size=2, gamma=.5)
    return p, opt, sched

def advance(p, opt, sched):
    rate_used = opt.param_groups[0]["lr"]
    opt.zero_grad(set_to_none=True)
    (p - 3).square().backward()
    opt.step()
    sched.step()  # Mỗi lần gọi ứng với một bước cập nhật đã xong.
    return rate_used

p, opt, sched = make_run(2.)
rates = [advance(p, opt, sched) for _ in range(3)]
snapshot = {"weight": p.item(), "optimizer": copy.deepcopy(opt.state_dict()),
            "scheduler": copy.deepcopy(sched.state_dict())}
current_rate = opt.param_groups[0]["lr"]
advance(p, opt, sched)

restored, restored_opt, restored_sched = make_run(snapshot["weight"])
restored_sched.load_state_dict(snapshot["scheduler"])
restored_opt.load_state_dict(snapshot["optimizer"])
advance(restored, restored_opt, restored_sched)

reset = torch.nn.Parameter(torch.tensor(snapshot["weight"], dtype=torch.float64))
reset_opt = torch.optim.Adam([reset], lr=current_rate)
reset_opt.zero_grad(set_to_none=True)
(reset - 3).square().backward()
reset_opt.step()
print("rate ba bước đầu:", rates)
print("liên tục / khôi phục / Adam mới:",
      *[round(v.item(), 8) for v in [p, restored, reset]])
print("rate kế tiếp liên tục / khôi phục:",
      opt.param_groups[0]["lr"], restored_opt.param_groups[0]["lr"])
assert torch.allclose(p, restored, atol=1e-12, rtol=0)
assert not torch.allclose(p, reset, atol=1e-6, rtol=0)

