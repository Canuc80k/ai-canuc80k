# -*- coding: utf-8 -*-
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

train = np.array([[10.0],[np.nan],[30.0]])
valid = np.array([[np.nan],[100.0]])
# Tất cả thống kê được học từ train.
prep = make_pipeline(SimpleImputer(strategy="median"),StandardScaler())
prep.fit(train)
print("Median train:",prep[0].statistics_.tolist())
print("Mean sau impute train:",prep[1].mean_.tolist())
print("Valid sau impute:",prep[0].transform(valid).ravel().tolist())
print("Valid sau scale:",prep.transform(valid).round(4).ravel().tolist())
assert prep[0].statistics_[0] == 20
# Sai protocol: không gọi fit/fit_transform trên valid.
