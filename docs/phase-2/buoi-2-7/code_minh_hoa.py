# -*- coding: utf-8 -*-
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

X,y = load_wine(return_X_y=True)
Xtr,Xva,ytr,yva = train_test_split(X,y,test_size=.3,stratify=y,random_state=42)
for kernel in ["linear","rbf"]:
    model = make_pipeline(StandardScaler(),SVC(kernel=kernel,C=1,gamma="scale"))
    model.fit(Xtr,ytr)
    print(kernel,"accuracy",round(model.score(Xva,yva),4),
          "support_vectors",int(model[-1].n_support_.sum()))
# decision_function là score/margin; không tự gọi nó là xác suất.
