# -*- coding: utf-8 -*-
import numpy as np
from sklearn.linear_model import LinearRegression

X = np.array([[0],[1],[2],[3]],dtype=float)
y = np.array([1,3,5,7],dtype=float)
model = LinearRegression().fit(X,y)
print("w:",model.coef_.round(6).tolist(),"b:",round(float(model.intercept_),6))
new = np.array([[4],[5]],dtype=float)
print("Dự đoán:",model.predict(new).round(6).tolist())
assert np.allclose(model.predict(new),[9,11])
# Đây là fixture tuyến tính chính xác; data thật thường có noise.
