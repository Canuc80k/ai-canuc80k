# -*- coding: utf-8 -*-
# Code mẫu — Sentence embedding

# Ví dụ 1: Độ dài vector làm kết quả tìm kiếm lệch
import numpy as np

def unit_rows(vectors):
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    if np.any(norms == 0):
        raise ValueError("Không tính cosine cho vector 0")
    return vectors / norms

query = np.array([[1., 1.]])
documents = np.array([[2., 2.], [10., 0.], [-1., -1.]])
dot = query @ documents.T
cosine = unit_rows(query) @ unit_rows(documents).T
print("dot chưa chuẩn hóa:", dot.round(3).tolist())
print("cosine:", cosine.round(3).tolist())
print("top-1 dot/cosine:", int(dot.argmax()), int(cosine.argmax()))
assert np.allclose(cosine, [[1, 1 / np.sqrt(2), -1]])
assert np.allclose(unit_rows(7 * query) @ unit_rows(documents).T, cosine)
try:
    unit_rows(np.array([[0., 0.]]))
except ValueError as error:
    print("query rỗng:", error)


# Ví dụ 2: Thêm PAD không được làm đổi phép lấy trung bình
import torch

torch.set_num_threads(1)

def masked_mean(hidden, keep_mask):
    if hidden.shape[:2] != keep_mask.shape:
        raise ValueError("Mask phải khớp hai trục batch và token")
    if not keep_mask.any(dim=1).all():
        raise ValueError("Có câu toàn PAD")
    weights = keep_mask.unsqueeze(-1).to(hidden.dtype)
    return (hidden * weights).sum(dim=1) / weights.sum(dim=1)

real_tokens = torch.tensor([[[2., 0.], [0., 2.]]])
padded = torch.cat([real_tokens, torch.full((1, 2, 2), 9.)], dim=1)
mask = torch.tensor([[True, True, False, False]])
correct = masked_mean(padded, mask)
print("mean cả PAD:", padded.mean(dim=1).tolist())
print("mean có mask:", correct.tolist())
print("shape sau pooling:", tuple(correct.shape))
print("thêm PAD không đổi:", torch.allclose(correct, masked_mean(real_tokens, mask[:, :2])))
assert torch.allclose(correct, torch.tensor([[1., 1.]]))
try:
    masked_mean(padded, torch.zeros_like(mask))
except ValueError as error:
    print("từ chối đầu vào:", error)


# Ví dụ 3: Phát hiện một thứ hạng chỉ đúng nhờ may
import numpy as np

document_vectors = np.eye(3)
query_vectors = np.array([[0.8, 0.2, 0.0], [0.0, 0.3, 0.7], [0.1, 0.2, 0.7]])
gold = np.array([0, 1, 2])
query_vectors /= np.linalg.norm(query_vectors, axis=1, keepdims=True)
scores = query_vectors @ document_vectors.T

def retrieval_metrics(scores, gold):
    order = np.argsort(-scores, axis=1, kind="stable")
    # stable chỉ quy định cách phá hòa, không thêm bằng chứng nào về độ liên quan.
    ranks = np.array([np.flatnonzero(row == label)[0] + 1
                      for row, label in zip(order, gold)])
    return ranks, (ranks <= 1).mean(), (ranks <= 2).mean(), (1 / ranks).mean()

ranks, r1, r2, mrr = retrieval_metrics(scores, gold)
print("score:", scores.round(3).tolist())
print("hạng tài liệu đúng:", ranks.tolist())
print(f"R@1={r1:.3f} R@2={r2:.3f} MRR={mrr:.3f}")
assert ranks.tolist() == [1, 2, 1]
assert np.isclose(mrr, (1 + 1 / 2 + 1) / 3)

empty_scores = np.zeros((1, 3))
print("argmax khi toàn 0:", int(empty_scores.argmax()))
print("có tín hiệu để trả kết quả:", bool(np.any(empty_scores != 0)))

