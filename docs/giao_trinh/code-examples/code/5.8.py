# -*- coding: utf-8 -*-
# Code mẫu — GAN và diffusion

# Ví dụ 1: Ở mỗi bước GAN, mạng nào được đổi?
import torch
from torch import nn

torch.set_num_threads(1)
torch.manual_seed(58)
generator = nn.Linear(1, 1)
discriminator = nn.Linear(1, 1)
opt_g = torch.optim.SGD(generator.parameters(), lr=0.1)
opt_d = torch.optim.SGD(discriminator.parameters(), lr=0.1)
criterion = nn.BCEWithLogitsLoss()
real = torch.tensor([[1.7], [1.9], [2.1], [2.3]])
noise = torch.tensor([[-1.], [0.], [1.], [2.]])
g_before = [p.detach().clone() for p in generator.parameters()]
d_before = [p.detach().clone() for p in discriminator.parameters()]
opt_d.zero_grad()
real_logits = discriminator(real)
fake_logits = discriminator(generator(noise).detach())
loss_d = criterion(real_logits, torch.ones_like(real_logits))
loss_d += criterion(fake_logits, torch.zeros_like(fake_logits))
loss_d.backward()
opt_d.step()
print("Bước D, loss:", round(loss_d.item(), 4))
print("G không gradient:", all(p.grad is None for p in generator.parameters()))
print("G giữ nguyên:", all(torch.equal(a, b) for a, b in zip(g_before, generator.parameters())))
print("D đã đổi:", any(not torch.equal(a, b) for a, b in zip(d_before, discriminator.parameters())))
assert all(p.grad is None for p in generator.parameters())

d_before = [p.detach().clone() for p in discriminator.parameters()]
g_before = [p.detach().clone() for p in generator.parameters()]
for p in discriminator.parameters():
    p.requires_grad_(False)
opt_g.zero_grad()
fake = generator(noise)
logits = discriminator(fake)
loss_g = criterion(logits, torch.ones_like(logits))
loss_g.backward()
gradient = generator.weight.grad.item()
opt_g.step()
for p in discriminator.parameters():
    p.requires_grad_(True)
print("Bước G, loss:", round(loss_g.item(), 4))
print("Gradient weight G:", round(gradient, 4))
print("D giữ nguyên:", all(torch.equal(a, b) for a, b in zip(d_before, discriminator.parameters())))
print("G đã đổi:", any(not torch.equal(a, b) for a, b in zip(g_before, generator.parameters())))
assert gradient != 0
assert all(torch.equal(a, b) for a, b in zip(d_before, discriminator.parameters()))
assert any(not torch.equal(a, b) for a, b in zip(g_before, generator.parameters()))


# Ví dụ 2: Thêm nhiễu, và sai số khi đảo ngược bị phóng đại
import numpy as np

clean, noise = 2.0, 0.5
for alpha_bar in [0.64, 0.04]:
    noisy = np.sqrt(alpha_bar) * clean + np.sqrt(1 - alpha_bar) * noise
    exact = (noisy - np.sqrt(1 - alpha_bar) * noise) / np.sqrt(alpha_bar)
    estimated_noise = noise + 0.1
    estimate = (noisy - np.sqrt(1 - alpha_bar) * estimated_noise) / np.sqrt(alpha_bar)
    print("alpha_bar", alpha_bar, "x_t/x0 đúng/x0 ước lượng:",
          [round(float(v), 4) for v in [noisy, exact, estimate]])
    assert np.isclose(exact, clean)

betas = np.array([0.1, 0.2, 0.3])
alpha_bars = np.cumprod(1 - betas)
print("alpha_bar theo lịch:", alpha_bars.round(4).tolist())
assert np.allclose(alpha_bars, [0.9, 0.72, 0.504])
assert np.all(np.diff(alpha_bars) < 0)


# Ví dụ 3: Học dự đoán nhiễu, rồi đi ngược theo cùng lịch
import torch
from torch import nn

torch.set_num_threads(1)
torch.manual_seed(580)
steps = 40
betas = torch.linspace(0.02, 0.18, steps)
alpha_bars = torch.cumprod(1 - betas, dim=0)
denoiser = nn.Sequential(nn.Linear(2, 24), nn.Tanh(), nn.Linear(24, 1))
optimizer = torch.optim.Adam(denoiser.parameters(), lr=0.01)

def batch(count):
    clean = (torch.randint(0, 2, (count, 1)) * 4 - 2).float() + 0.2 * torch.randn(count, 1)
    times = torch.randint(0, steps, (count,))
    noise = torch.randn(count, 1)
    a = alpha_bars[times, None]
    noisy = a.sqrt() * clean + (1 - a).sqrt() * noise
    return torch.cat([noisy, times[:, None] / (steps - 1)], dim=1), noise

valid_x, valid_noise = batch(128)
with torch.no_grad():
    before = nn.functional.mse_loss(denoiser(valid_x), valid_noise).item()
for update in range(180):
    x, target = batch(64)
    optimizer.zero_grad()
    loss = nn.functional.mse_loss(denoiser(x), target)
    loss.backward()
    optimizer.step()
denoiser.eval()
with torch.no_grad():
    after = nn.functional.mse_loss(denoiser(valid_x), valid_noise).item()
    baseline = valid_noise.square().mean().item()
print("Noise MSE trước/sau/baseline 0:", [round(v, 4) for v in [before, after, baseline]])
print("alpha_bar cuối:", round(alpha_bars[-1].item(), 4))
assert after < before and after < baseline

torch.manual_seed(581)
samples = torch.randn(8, 1)
with torch.no_grad():
    for t in reversed(range(steps)):
        current = alpha_bars[t]
        previous = alpha_bars[t - 1] if t > 0 else torch.tensor(1.0)
        time_feature = torch.full_like(samples, t / (steps - 1))
        predicted_noise = denoiser(torch.cat([samples, time_feature], dim=1))
        estimated_clean = (samples - (1 - current).sqrt() * predicted_noise) / current.sqrt()
        samples = previous.sqrt() * estimated_clean + (1 - previous).sqrt() * predicted_noise
print("Tám mẫu sinh một chiều:", [round(v, 3) for v in samples.flatten().tolist()])
print("Mẫu âm/dương:", int((samples < 0).sum()), int((samples >= 0).sum()))
assert torch.isfinite(samples).all()

