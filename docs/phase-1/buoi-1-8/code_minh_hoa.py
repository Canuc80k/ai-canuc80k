# -*- coding: utf-8 -*-
import numpy as np

x = np.array([1,2,3,100],dtype=float)
print("Mean:",x.mean(),"Median:",np.median(x))
print("Std population:",round(x.std(ddof=0),4))
# 20 vật lỗi, 80 vật tốt; detector bắt đúng 18 và báo nhầm 8.
tp,fn,fp,tn = 18,2,8,72
print("P(canh bao|loi):",tp/(tp+fn))
print("P(loi|canh bao):",round(tp/(tp+fp),6))
print("Hai xác suất có điều kiện này không bằng nhau.")
assert x.mean()==26.5 and np.median(x)==2.5
