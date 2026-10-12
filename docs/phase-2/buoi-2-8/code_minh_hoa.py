# -*- coding: utf-8 -*-
import numpy as np
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

X,y = load_iris(return_X_y=True)
X = StandardScaler().fit_transform(X)  # Đây là lab visualization, không test model.
pca = PCA(n_components=2).fit(X)
Z = pca.transform(X)
print("PCA shape:",Z.shape)
print("Explained variance:",pca.explained_variance_ratio_.round(4).tolist())
T = TSNE(n_components=2,perplexity=20,max_iter=250,
         random_state=42,init="pca",learning_rate="auto").fit_transform(X)
print("t-SNE shape:",T.shape,"finite:",bool(np.isfinite(T).all()))
# UMAP là thư viện riêng; code đầy đủ nằm trong nguồn của bài.
# Phép chiếu đẹp không chứng minh một classifier tổng quát tốt.
