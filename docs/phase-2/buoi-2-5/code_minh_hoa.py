# -*- coding: utf-8 -*-
from sklearn.datasets import make_moons
from sklearn.tree import DecisionTreeClassifier,export_text
from sklearn.model_selection import train_test_split

X,y = make_moons(n_samples=80,noise=.35,random_state=42)
Xtr,Xva,ytr,yva = train_test_split(X,y,test_size=.35,stratify=y,random_state=27)
for depth in [1,3,None]:
    model = DecisionTreeClassifier(max_depth=depth,random_state=42).fit(Xtr,ytr)
    print("depth",depth,"train",round(model.score(Xtr,ytr),4),
          "valid",round(model.score(Xva,yva),4))
    if depth==1:
        print(export_text(model,feature_names=["x1","x2"]).strip())
