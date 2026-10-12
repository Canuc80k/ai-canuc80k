# -*- coding: utf-8 -*-
import numpy as np
from sklearn.linear_model import LinearRegression,Ridge,Lasso

X = np.array([[0,0],[1,1],[2,2],[3,3],[4,4]],dtype=float)
y = np.array([0,2,4,6,8],dtype=float)
print("Hai features ở đây giống nhau hoàn toàn.")
for model in [LinearRegression(),Ridge(alpha=10),Lasso(alpha=0.5)]:
    model.fit(X,y)
    print(type(model).__name__,model.coef_.round(4).tolist())
print("L1([1,1]):",np.abs([1,1]).sum())
print("L2 squared([1,1]):",np.square([1,1]).sum())
# Không chọn penalty bằng điểm test.
