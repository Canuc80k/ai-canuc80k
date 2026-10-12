# -*- coding: utf-8 -*-
# MLP và backpropagation — chạy các bước như notebook từ trên xuống.

# Bước 1
import numpy as np
import torch

torch.set_num_threads(1)
torch.manual_seed(11)
np.set_printoptions(precision=4, suppress=True)
X_xor = np.array([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
hidden = np.maximum(X_xor @ np.ones((2, 2)) + [0., -1.], 0.)
print(hidden)
print(hidden @ np.array([1., -2.]))

# Bước 2
X = np.array([[1., 2.], [2., -1.]])
Y = np.array([[1.], [0.]])
params = [np.array([[.2, -.3], [.4, .1]]), np.array([.1, .2]),
          np.array([[.5], [-.4]]), np.array([.05])]

def forward(params):
    W1, b1, W2, b2 = params
    Z1 = X @ W1 + b1
    H = np.maximum(Z1, 0)
    P = H @ W2 + b2
    return P, (Z1, H)

def objective(params):
    P, _ = forward(params)
    assert P.shape == Y.shape
    return np.mean((P - Y) ** 2)

def backward(params):
    P, (Z1, H) = forward(params)
    G2 = 2 * (P - Y) / len(X)
    G1 = (G2 @ params[2].T) * (Z1 > 0)
    return [X.T @ G1, G1.sum(axis=0), H.T @ G2, G2.sum(axis=0)]

print(forward(params)[0].ravel())
print(round(objective(params), 6))
for g in backward(params):
    print(g)

# Bước 3
def numerical_gradient(params, eps=1e-5):
    answer = []
    for p in params:
        g = np.zeros_like(p)
        for index in np.ndindex(p.shape):
            old = p[index]
            p[index] = old + eps
            plus = objective(params)
            p[index] = old - eps
            minus = objective(params)
            p[index] = old
            g[index] = (plus - minus) / (2 * eps)
        answer.append(g)
    return answer

manual = backward(params)
numeric = numerical_gradient(params)
print('numeric match:', all(np.allclose(a, b, atol=1e-8)
                            for a, b in zip(manual, numeric)))

tp = [torch.tensor(p, dtype=torch.float64, requires_grad=True) for p in params]
tx, ty = torch.tensor(X), torch.tensor(Y)
pred = torch.relu(tx @ tp[0] + tp[1]) @ tp[2] + tp[3]
((pred - ty) ** 2).mean().backward()
print('autograd match:', all(np.allclose(g, p.grad.numpy(), atol=1e-10)
                            for g, p in zip(manual, tp)))
updated = [p - .05 * g for p, g in zip(params, manual)]
print(round(objective(params), 6), round(objective(updated), 6))

# Bước 4
model = torch.nn.Sequential(torch.nn.Linear(2, 3), torch.nn.ReLU(),
                            torch.nn.Linear(3, 1))
print(tuple(model(torch.zeros(4, 2)).shape))
print(sum(p.numel() for p in model.parameters()))
