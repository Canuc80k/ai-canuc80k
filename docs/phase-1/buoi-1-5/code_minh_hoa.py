# -*- coding: utf-8 -*-
from sklearn.metrics import confusion_matrix,precision_score,recall_score,f1_score,roc_auc_score

# Positive=1; xác suất dùng cho AUC, nhãn dùng cho F1.
y = [1,1,0,0]
prob = [0.9,0.4,0.6,0.1]
pred = [int(p>=0.5) for p in prob]
print("pred:",pred)
print("Confusion [TN FP; FN TP]:",confusion_matrix(y,pred).tolist())
print("Precision:",precision_score(y,pred,zero_division=0))
print("Recall:",recall_score(y,pred,zero_division=0))
print("F1:",f1_score(y,pred,zero_division=0))
print("ROC AUC:",roc_auc_score(y,prob))
assert f1_score(y,pred)==0.5
