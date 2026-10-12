# -*- coding: utf-8 -*-
# Thư viện bổ sung: umap-learn. Đây là code UMAP thật, không PCA đổi tên.
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
import umap
X,y=load_iris(return_X_y=True)
X=StandardScaler().fit_transform(X)
model=umap.UMAP(n_neighbors=15,min_dist=.1,n_components=2,random_state=42)
Z=model.fit_transform(X)
print("Input:",X.shape,"UMAP:",Z.shape)
print("Năm điểm đầu:",Z[:5])
# Lab visualization: không dùng hình này thay classifier validation.
