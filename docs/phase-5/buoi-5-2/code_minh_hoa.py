# -*- coding: utf-8 -*-
import numpy as np

tokens=np.array([[1.,0.],[0.,1.],[9.,9.]])
mask=np.array([1,1,0],dtype=float)
# Padding không được tham gia mean pooling.
pooled=(tokens*mask[:,None]).sum(axis=0)/mask.sum()
print("Mean pooling có mask:",pooled.tolist())
print("Mean sai nếu tính padding:",tokens.mean(axis=0).tolist())
options=np.array([[1.,0.],[0.,1.],[1.,1.]])
norm=lambda a:a/np.linalg.norm(a,axis=-1,keepdims=True)
scores=norm(options)@norm(pooled)
print("Cosine:",scores.round(4).tolist())
assert np.allclose(pooled,[.5,.5])
