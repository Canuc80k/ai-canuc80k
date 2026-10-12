# -*- coding: utf-8 -*-
import numpy as np
from sklearn.datasets import make_moons
from sklearn.cluster import KMeans,DBSCAN,AgglomerativeClustering,SpectralClustering
from sklearn.metrics import adjusted_rand_score

X,y = make_moons(n_samples=120,noise=.05,random_state=42)
models = [KMeans(n_clusters=2,n_init=10,random_state=42),
          DBSCAN(eps=.25,min_samples=4),AgglomerativeClustering(n_clusters=2),
          SpectralClustering(2,affinity="nearest_neighbors",random_state=42)]
for model in models:
    labels = model.fit_predict(X)
    # y chỉ dùng sau khi fit, không đưa vào thuật toán.
    print(type(model).__name__,"clusters",len(set(labels)-{-1}),
          "noise",int((labels==-1).sum()),"ARI",round(adjusted_rand_score(y,labels),4))
