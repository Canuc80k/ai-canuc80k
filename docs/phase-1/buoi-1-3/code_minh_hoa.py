# -*- coding: utf-8 -*-
import numpy as np
from sklearn.model_selection import GroupKFold,StratifiedKFold

# Hai ảnh cùng con vật phải thuộc cùng một group khi đánh giá cá thể mới.
ids = np.arange(8)
groups = np.array([0,0,1,1,2,2,3,3])
y = np.array([0,0,1,1,0,0,1,1])
X = ids.reshape(-1,1)
print("Group folds:")
for train,valid in GroupKFold(n_splits=2).split(X,y,groups):
    print("train",train.tolist(),"valid",valid.tolist())
    assert set(groups[train]).isdisjoint(set(groups[valid]))
print("Stratified giữ tỉ lệ lớp, không tự giữ group:")
for train,valid in StratifiedKFold(2,shuffle=True,random_state=42).split(X,y):
    overlap = sorted(set(groups[train]) & set(groups[valid]))
    print("groups trùng:",overlap)
