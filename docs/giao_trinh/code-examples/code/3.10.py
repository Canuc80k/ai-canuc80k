# -*- coding: utf-8 -*-
# Code mẫu — Autoencoder

# Ví dụ 1: Tính tay một nút thắt
import numpy as np

sample = np.array([0.9, 0.1])
code = sample.mean()
reconstructed = np.array([code, code])
mse = np.mean((reconstructed - sample) ** 2)
large_on_line = np.array([100., 100.])
large_code = large_on_line.mean()
large_reconstruction = np.array([large_code, large_code])
print("sample -> code -> reconstruction:", sample.tolist(), round(float(code), 4), reconstructed.tolist())
print("reconstruction MSE:", round(float(mse), 4))
print("large sample MSE:", round(float(np.mean((large_reconstruction - large_on_line) ** 2)), 4))
assert np.allclose(reconstructed, [0.5, 0.5])
assert np.isclose(mse, 0.16)
assert np.allclose(large_reconstruction, large_on_line)


# Ví dụ 2: So autoencoder tuyến tính với PCA
import numpy as np
import torch
from torch import nn

torch.set_num_threads(1)
torch.manual_seed(3102)
generator = torch.Generator().manual_seed(3102)
direction = torch.tensor([1., 2., -1., 0.5])

def make_normal(size):
    t = torch.randn(size, 1, generator=generator)
    clean = t * direction
    noisy = clean + 0.03 * torch.randn(size, 4, generator=generator)
    return noisy

raw_train = make_normal(64)
raw_valid = make_normal(24)
mean = raw_train.mean(dim=0)
scale = raw_train.std(dim=0, unbiased=False).clamp_min(1e-6)
train = (raw_train - mean) / scale
valid = (raw_valid - mean) / scale
print("train/valid shapes:", tuple(train.shape), tuple(valid.shape))

train_np = train.numpy()
_, singular_values, vt = np.linalg.svd(train_np, full_matrices=False)
axis = vt[0]
pca_latent = train_np @ axis
pca_reconstruction = pca_latent[:, None] * axis[None, :]
pca_mse = np.mean((pca_reconstruction - train_np) ** 2)
print("PCA train MSE:", round(float(pca_mse), 6))
print("PCA variance fraction:", round(float(
    singular_values[0] ** 2 / np.sum(singular_values ** 2)
), 6))

class LinearAutoencoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = nn.Linear(4, 1, bias=False)
        self.decoder = nn.Linear(1, 4, bias=False)

    def forward(self, x):
        return self.decoder(self.encoder(x))

autoencoder = LinearAutoencoder()
optimizer = torch.optim.Adam(autoencoder.parameters(), lr=0.04)
initial = (autoencoder(train) - train).square().mean().item()
for _ in range(180):
    optimizer.zero_grad(set_to_none=True)
    reconstruction = autoencoder(train)
    loss = (reconstruction - train).square().mean()
    assert torch.isfinite(loss)
    loss.backward()
    optimizer.step()
autoencoder.eval()
with torch.no_grad():
    final = (autoencoder(train) - train).square().mean().item()
    valid_loss = (autoencoder(valid) - valid).square().mean().item()
    latent_shape = tuple(autoencoder.encoder(valid).shape)
print("autoencoder train MSE:", round(initial, 6), "->", round(final, 6))
print("autoencoder validation MSE:", round(valid_loss, 6))
print("latent shape:", latent_shape)
assert latent_shape == (24, 1)
assert final < initial


# Ví dụ 3: Nút thắt hẹp và rộng khi dùng để dò bất thường
import torch
from torch import nn

torch.set_num_threads(1)
torch.manual_seed(3103)
direction = torch.tensor([1., 2., -1., 0.5])

def make_normal(size, seed):
    generator = torch.Generator().manual_seed(seed)
    t = torch.linspace(-1.5, 1.5, size).unsqueeze(1)
    clean = t * direction
    return clean + 0.03 * torch.randn(size, 4, generator=generator)

normal_train = make_normal(48, 1)
normal_valid = make_normal(16, 2)
normal_test = make_normal(16, 3)
anomaly_test = make_normal(16, 4)
anomaly_test[:, 1] += 1.5
print("normal/anomaly shapes:", tuple(normal_test.shape), tuple(anomaly_test.shape))

class BottleneckAutoencoder(nn.Module):
    def __init__(self, latent_width):
        super().__init__()
        self.encoder = nn.Linear(4, latent_width, bias=False)
        self.decoder = nn.Linear(latent_width, 4, bias=False)

    def forward(self, x):
        return self.decoder(self.encoder(x))

def train_autoencoder(model, data, steps, learning_rate):
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    for _ in range(steps):
        optimizer.zero_grad(set_to_none=True)
        loss = (model(data) - data).square().mean()
        loss.backward()
        optimizer.step()
    return model.eval()

narrow = train_autoencoder(BottleneckAutoencoder(1), normal_train, 220, 0.04)
wide = BottleneckAutoencoder(4)
with torch.no_grad():
    wide.encoder.weight.copy_(torch.eye(4))
    wide.decoder.weight.copy_(torch.eye(4))
wide.eval()
with torch.no_grad():
    narrow_train_mse = (narrow(normal_train) - normal_train).square().mean().item()
    identity_check = torch.allclose(wide(anomaly_test), anomaly_test)
print("narrow train MSE:", round(narrow_train_mse, 6))
print("wide identity reconstructs anomaly exactly:", identity_check)
assert identity_check

def score(model, data):
    with torch.no_grad():
        return (model(data) - data).square().mean(dim=1)

for name, model in [("latent=1", narrow), ("latent=4", wide)]:
    valid_score = score(model, normal_valid)
    normal_score = score(model, normal_test)
    anomaly_score = score(model, anomaly_test)
    threshold = torch.quantile(valid_score, 0.9)
    normal_flagged = int((normal_score > threshold).sum())
    flagged = int((anomaly_score > threshold).sum())
    print(name, "valid p90:", round(float(threshold), 6),
          "normal median:", round(float(normal_score.median()), 6),
          "anomaly median:", round(float(anomaly_score.median()), 6),
          "normal flagged:", normal_flagged, "/", len(normal_score),
          "anomaly flagged:", flagged, "/", len(anomaly_score))
    assert torch.isfinite(valid_score).all()

