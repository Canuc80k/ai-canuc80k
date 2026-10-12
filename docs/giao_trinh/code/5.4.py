# -*- coding: utf-8 -*-
# Vision Transformer — chạy các bước như notebook từ trên xuống.

# Bước 1
import torch
from torch import nn

torch.set_num_threads(1)
torch.manual_seed(54)
images = torch.arange(16, dtype=torch.float32).reshape(1, 1, 4, 4)
patch_size = 2
windows = images.unfold(2, patch_size, patch_size)
windows = windows.unfold(3, patch_size, patch_size)
patches = windows.permute(0, 2, 3, 1, 4, 5).reshape(1, 4, 4)
print(patches[0].to(torch.int64).numpy())
print(tuple(patches.shape))

# Bước 2
projection = nn.Linear(4, 3)
with torch.no_grad():
    projection.weight.copy_(torch.tensor([[1., 0., 0., 0.],
                                          [0., 1., 0., 0.],
                                          [0.25, 0.25, 0.25, 0.25]]))
    projection.bias.zero_()
tokens = projection(patches)

patch_conv = nn.Conv2d(1, 3, kernel_size=2, stride=2)
with torch.no_grad():
    patch_conv.weight.copy_(projection.weight.reshape(3, 1, 2, 2))
    patch_conv.bias.copy_(projection.bias)
    conv_tokens = patch_conv(images).flatten(2).transpose(1, 2)
print(tokens[0].detach().tolist())
print(torch.allclose(tokens, conv_tokens))

# Bước 3
encoder = nn.TransformerEncoderLayer(
    d_model=3, nhead=1, dim_feedforward=6,
    dropout=0.0, batch_first=True,
)
encoder.eval()
permutation = torch.tensor([2, 0, 3, 1])
positions = torch.tensor([[[0.4, 0.0, 0.0],
                           [0.0, 0.4, 0.0],
                           [0.0, 0.0, 0.4],
                           [0.2, -0.3, 0.1]]])
with torch.no_grad():
    pooled = encoder(tokens).mean(dim=1)
    shuffled = encoder(tokens[:, permutation]).mean(dim=1)
    with_position = encoder(tokens + positions).mean(dim=1)
    shuffled_content = encoder(tokens[:, permutation] + positions).mean(dim=1)
print("without position:", torch.allclose(pooled, shuffled, atol=1e-5))
print("with fixed positions:", torch.allclose(with_position, shuffled_content, atol=1e-5))

# Bước 4
import torch.nn.functional as F

def resize_position_table(table, old_grid, new_grid):
    cls_part, grid_part = table[:, :1], table[:, 1:]
    dim = table.shape[-1]
    grid = grid_part.reshape(1, old_grid, old_grid, dim).permute(0, 3, 1, 2)
    grid = F.interpolate(grid, size=(new_grid, new_grid),
                         mode="bilinear", align_corners=True)
    grid_part = grid.permute(0, 2, 3, 1).reshape(1, new_grid * new_grid, dim)
    return torch.cat([cls_part, grid_part], dim=1)

rows, cols = torch.meshgrid(torch.arange(4.0), torch.arange(4.0), indexing="ij")
coords = torch.stack([rows, cols], dim=-1).reshape(1, 16, 2)
table = torch.cat([torch.full((1, 1, 2), -1.0), coords], dim=1)
resized = resize_position_table(table, old_grid=4, new_grid=7)
print(tuple(table.shape), "->", tuple(resized.shape))
print("CLS:", resized[0, 0].tolist())
print("row of first column:", resized[0, 1:, 0].reshape(7, 7)[:, 0].tolist())
