# -*- coding: utf-8 -*-
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

X = np.array([[0],[2],[10]],dtype=float)
y = np.array([0,0,1])
query = np.array([[3.0]])
for k in [1,3]:
    model = KNeighborsClassifier(n_neighbors=k).fit(X,y)
    distance,index = model.kneighbors(query)
    print("k",k,"neighbors",index[0].tolist(),"distance",distance[0].tolist())
    print("class:",int(model.predict(query)[0]))
assert KNeighborsClassifier(1).fit(X,y).predict(query)[0]==0
