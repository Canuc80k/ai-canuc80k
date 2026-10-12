# -*- coding: utf-8 -*-

# f(w)=(w-3)^2, gradient=2*(w-3).
w = 0.0
learning_rate = 0.1
print("step | w | loss")
for step in range(5):
    loss = (w-3)**2
    print(step,round(w,4),round(loss,4))
    grad = 2*(w-3)
    w = w-learning_rate*grad
print("w sau 5 updates:",round(w,6))
assert abs(w-2.01696)<1e-8
