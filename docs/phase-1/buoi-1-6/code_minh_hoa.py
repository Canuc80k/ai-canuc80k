# -*- coding: utf-8 -*-
import numpy as np

y = np.array([1.0,3.0])
pred = np.array([2.0,5.0])
error = pred-y
mae = np.abs(error).mean()
mse = (error**2).mean()
rmse = np.sqrt(mse)
print("Sai số:",error.tolist())
print("MAE:",mae)
print("MSE:",mse)
print("RMSE:",round(rmse,6))
assert mae==1.5 and mse==2.5
