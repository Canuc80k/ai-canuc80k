# -*- coding: utf-8 -*-
# Self-supervised và CLIP — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np

def normalize_rows(vectors):
    lengths = np.linalg.norm(vectors, axis=1, keepdims=True)
    assert np.all(lengths > 0)
    return vectors / lengths

image_vectors = normalize_rows(np.array([[1., 0.],
                                        [0., 1.],
                                        [-1., 0.]]))
text_vectors = normalize_rows(np.array([[0.9, 0.1],
                                       [0.1, 0.9],
                                       [-0.9, 0.1]]))
similarities = image_vectors @ text_vectors.T
print(similarities.round(4))
print("best text for each image:", similarities.argmax(axis=1).tolist())
print("best image for text 1:", int(similarities[:, 1].argmax()))

# Bước 2
import torch
import torch.nn.functional as F

torch.set_num_threads(1)
logits = torch.tensor([[2., 0.2, -1.],
                       [0.1, 2., 0.3],
                       [-1., 0.2, 2.]], requires_grad=True)
targets = torch.arange(3)
loss_image = F.cross_entropy(logits, targets)
loss_text = F.cross_entropy(logits.T, targets)
contrastive_loss = (loss_image + loss_text) / 2
contrastive_loss.backward()
print("symmetric loss:", round(contrastive_loss.item(), 4))
print("diagonal gradients:", [round(float(v), 4) for v in logits.grad.diag()])
print("negative gradient [0,1]:", round(logits.grad[0, 1].item(), 4))

# Bước 3
row_scores = torch.tensor([0.8, 0.7, 0., 0., 0., 0., 0., 0.])  # cột 0 là positive
for tau in [1.0, 0.5, 0.1]:
    probabilities = (row_scores / tau).softmax(0)
    push = probabilities[1:] / tau          # lực đẩy lên từng negative
    hard_share = push[0] / push.sum()
    print(f"tau={tau}: loss {-probabilities[0].log().item():.3f}, "
          f"hard-negative share {hard_share.item():.3f}")

# Bước 4
import copy
import math
import torch.nn as nn

SIZE = 32
grid_y, grid_x = np.mgrid[0:SIZE, 0:SIZE] + 0.5   # tâm các pixel

def draw_shape(label, rng):
    cx, cy = rng.uniform(10, 22, size=2)
    radius = rng.uniform(5, 9)
    angle = rng.uniform(0, 2 * np.pi)
    if label == 0:                                   # hình tròn
        mask = (grid_x - cx) ** 2 + (grid_y - cy) ** 2 <= radius ** 2
    else:
        if label == 1:                               # tam giác không đều
            angles = angle + np.array([0, 2, 4]) * np.pi / 3 + rng.uniform(-0.5, 0.5, 3)
            corners = np.stack([np.cos(angles), np.sin(angles)], axis=1) * radius
        else:                                        # chữ nhật xoay
            half_w, half_h = radius * rng.uniform(0.6, 1.0, size=2)
            corners = np.array([[-half_w, -half_h], [half_w, -half_h],
                                [half_w, half_h], [-half_w, half_h]])
            rotation = np.array([[np.cos(angle), -np.sin(angle)],
                                 [np.sin(angle), np.cos(angle)]])
            corners = corners @ rotation.T
        corners = corners + [cx, cy]
        mask = np.ones((SIZE, SIZE), dtype=bool)     # đa giác lồi: cùng phía mọi cạnh
        for (x0, y0), (x1, y1) in zip(corners, np.roll(corners, -1, axis=0)):
            mask &= (x1 - x0) * (grid_y - y0) - (y1 - y0) * (grid_x - x0) >= 0
    image = np.zeros((SIZE, SIZE), dtype=np.float32)
    image[mask] = rng.uniform(0.4, 1.0)              # độ sáng ngẫu nhiên
    return image

def make_shapes(n, rng):
    labels = rng.integers(0, 3, size=n)
    images = np.stack([draw_shape(label, rng) for label in labels])
    return torch.tensor(images).unsqueeze(1), labels

rng = np.random.default_rng(0)
train_images, train_labels = make_shapes(1000, rng)
test_images, test_labels = make_shapes(300, rng)
labeled = slice(0, 200)                              # chỉ 200 ảnh đầu được dùng nhãn
print("train:", tuple(train_images.shape), "test:", tuple(test_images.shape))
print("labels in the 200 labeled images:", np.bincount(train_labels[labeled]).tolist())

# Bước 5
def augment(images, generator):
    batch = images.shape[0]
    angle = torch.rand(batch, generator=generator) * 2 * math.pi
    scale = 0.8 + 0.4 * torch.rand(batch, generator=generator)
    shift = (torch.rand(batch, 2, generator=generator) - 0.5) * 0.4
    cos, sin = torch.cos(angle) / scale, torch.sin(angle) / scale
    theta = torch.stack([torch.stack([cos, -sin, shift[:, 0]], dim=1),
                         torch.stack([sin, cos, shift[:, 1]], dim=1)], dim=1)
    grid = F.affine_grid(theta, list(images.shape), align_corners=False)
    views = F.grid_sample(images, grid, align_corners=False)
    brightness = 0.6 + 0.8 * torch.rand(batch, 1, 1, 1, generator=generator)
    return views * brightness

def conv_block(c_in, c_out):
    return [nn.Conv2d(c_in, c_out, 3, padding=1), nn.BatchNorm2d(c_out), nn.ReLU()]

def make_encoder():
    return nn.Sequential(*conv_block(1, 16), nn.MaxPool2d(2),
                         *conv_block(16, 32), nn.MaxPool2d(2),
                         *conv_block(32, 64), nn.AdaptiveAvgPool2d(1), nn.Flatten())

def nt_xent(z1, z2, temperature):
    z = F.normalize(torch.cat([z1, z2]), dim=1)      # 2N view, mỗi hàng dài 1
    n = z1.shape[0]
    logits = z @ z.T / temperature
    logits.fill_diagonal_(float("-inf"))             # một view không tự so với chính nó
    targets = torch.cat([torch.arange(n, 2 * n), torch.arange(n)])   # partner
    return F.cross_entropy(logits, targets)

# Bước 6
torch.manual_seed(0)
encoder = make_encoder()
random_encoder = copy.deepcopy(encoder)              # cùng kiến trúc, chưa train
projection = nn.Sequential(nn.Linear(64, 64), nn.ReLU(), nn.Linear(64, 32))
optimizer = torch.optim.Adam([*encoder.parameters(), *projection.parameters()], lr=1e-3)
generator = torch.Generator().manual_seed(0)
batch_size, temperature = 125, 0.2
print(f"chance loss log(2N-1): {math.log(2 * batch_size - 1):.3f}")
for epoch in range(1, 11):
    encoder.train()
    projection.train()
    order = torch.randperm(len(train_images), generator=generator)
    losses = []
    for start in range(0, len(order), batch_size):
        batch = train_images[order[start:start + batch_size]]   # không dùng nhãn
        z1 = projection(encoder(augment(batch, generator)))
        z2 = projection(encoder(augment(batch, generator)))
        loss = nt_xent(z1, z2, temperature)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        losses.append(loss.item())
    if epoch in (1, 5, 10):
        print(f"epoch {epoch}: loss {np.mean(losses):.3f}")

# Bước 7
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

def embed(model, images):
    model.eval()
    with torch.no_grad():
        return model(images).numpy()

def probe_f1(train_features, test_features):
    probe = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
    probe.fit(train_features, train_labels[labeled])
    return f1_score(test_labels, probe.predict(test_features), average="macro")

def same_shape_rate(features, k=5):
    unit = F.normalize(torch.tensor(features), dim=1)
    scores = unit @ unit.T
    scores.fill_diagonal_(float("-inf"))
    neighbors = scores.topk(k, dim=1).indices.numpy()
    return (test_labels[neighbors] == test_labels[:, None]).mean()

feature_sets = {
    "pixels": (train_images[labeled].flatten(1).numpy(), test_images.flatten(1).numpy()),
    "random encoder": (embed(random_encoder, train_images[labeled]),
                       embed(random_encoder, test_images)),
    "contrastive": (embed(encoder, train_images[labeled]), embed(encoder, test_images)),
}
print(f"{'features':<15} probe F1  same shape@5")
for name, (train_features, test_features) in feature_sets.items():
    print(f"{name:<15} {probe_f1(train_features, test_features):.3f}     "
          f"{same_shape_rate(test_features):.3f}")
