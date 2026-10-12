# -*- coding: utf-8 -*-
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,HistGradientBoostingClassifier

X,y = load_breast_cancer(return_X_y=True)
Xtr,Xva,ytr,yva = train_test_split(X,y,test_size=.25,stratify=y,random_state=42)
models = [DecisionTreeClassifier(random_state=42),
          RandomForestClassifier(n_estimators=30,max_depth=5,random_state=42),
          HistGradientBoostingClassifier(max_iter=30,max_leaf_nodes=7,random_state=42)]
for model in models:
    model.fit(Xtr,ytr)
    print(type(model).__name__,"validation_accuracy",round(model.score(Xva,yva),4))
# Các điểm ở đây chỉ là kết quả một split, không benchmark tổng quát.
