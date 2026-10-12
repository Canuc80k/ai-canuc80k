# -*- coding: utf-8 -*-
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score

# Feature là năng lượng dải thấp/cao của tones tổng hợp.
X=np.array([[8,1],[9,2],[7,1],[1,8],[2,9],[1,7]],dtype=float)
y=np.array([0,0,0,1,1,1])
model=LogisticRegression(random_state=42).fit(X,y)
test=np.array([[8,2],[2,8]])
true=[0,1]; pred=model.predict(test)
print("Predictions:",pred.tolist(),"Macro F1:",f1_score(true,pred,average="macro"))
assert pred.tolist()==true
# Tones không thay giọng nói thật: IOAI Speech dùng spectrogram có sẵn, không features này.
