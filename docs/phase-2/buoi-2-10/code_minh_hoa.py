# -*- coding: utf-8 -*-
from sklearn.datasets import load_wine
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split,StratifiedKFold,GridSearchCV

X,y = load_wine(return_X_y=True)
Xtr,Xte,ytr,yte = train_test_split(X,y,test_size=.25,stratify=y,random_state=42)
pipe = make_pipeline(StandardScaler(),KNeighborsClassifier())
cv = StratifiedKFold(3,shuffle=True,random_state=42)
search = GridSearchCV(pipe,{"kneighborsclassifier__n_neighbors":[1,3,7]},
                      cv=cv,scoring="f1_macro")
search.fit(Xtr,ytr)  # Test không đi vào search.
print("Best params:",search.best_params_)
print("Mean CV F1:",round(search.best_score_,4))
print("Final test F1 macro:",round(search.score(Xte,yte),4))
# search.score ở đây dùng f1_macro vì search được đặt scoring đó.
