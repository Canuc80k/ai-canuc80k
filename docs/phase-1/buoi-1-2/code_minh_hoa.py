# -*- coding: utf-8 -*-
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# Cùng dữ liệu và split như ví dụ của thầy; đây là dữ liệu tổng hợp.
X,y = make_moons(n_samples=80, noise=0.35, random_state=42)
Xtr,Xva,ytr,yva = train_test_split(X,y,test_size=0.35,
                                 stratify=y,random_state=27)
print("depth | train_accuracy | valid_accuracy")
results = []
for depth in [1,3,10,None]:
    model = DecisionTreeClassifier(max_depth=depth,random_state=42)
    model.fit(Xtr,ytr)
    train_score = model.score(Xtr,ytr)
    valid_score = model.score(Xva,yva)
    results.append([str(depth),train_score,valid_score])
    print(depth, round(train_score,4), round(valid_score,4))
assert len(Xtr)==52 and len(Xva)==28
