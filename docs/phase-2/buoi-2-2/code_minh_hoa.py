# -*- coding: utf-8 -*-
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X = np.array([[-2],[-1],[1],[2]],dtype=float)
y = np.array([0,0,1,1])
model = make_pipeline(StandardScaler(),LogisticRegression(random_state=42))
model.fit(X,y)
new = np.array([[-1.5],[0],[1.5]])
print("classes:",model[-1].classes_.tolist())
print("P(y=1):",model.predict_proba(new)[:,1].round(4).tolist())
print("predict:",model.predict(new).tolist())
# Mô hình học logits; threshold là quyết định sau đó.
assert model.predict(new)[0]==0 and model.predict(new)[2]==1
