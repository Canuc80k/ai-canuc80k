# -*- coding: utf-8 -*-
import numpy as np

# X: hai mẫu, hai features. W biến mỗi mẫu thành một số.
X = np.array([[1,2],[3,4]],dtype=float)
w = np.array([2,-1],dtype=float)
b = 1.0
pred = X@w+b
print("X shape:",X.shape,"w shape:",w.shape)
print("X @ w:",(X@w).tolist())
print("X @ w + b:",pred.tolist())
# Cosine chỉ định nghĩa trực tiếp khi norm khác 0.
u,v = np.array([1,0]),np.array([1,1])
cosine = u@v/(np.linalg.norm(u)*np.linalg.norm(v))
print("Cosine:",round(float(cosine),6))
assert pred.tolist()==[1,3]
