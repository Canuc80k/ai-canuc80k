# -*- coding: utf-8 -*-
import numpy as np
from sklearn.dummy import DummyClassifier

# Mỗi dòng X là một mẫu, mỗi cột là một feature.
X_train = np.array([[1,2],[2,2],[3,4],[5,6]])
y_train = np.array([0,0,0,1])
X_new = np.array([[4,3],[8,7]])
# Baseline cố ý đơn giản: dự đoán lớp phổ biến trong train.
model = DummyClassifier(strategy="most_frequent")
model.fit(X_train, y_train)
pred = model.predict(X_new)
print("Train shape:", X_train.shape)
print("Target:", y_train)
print("Dự đoán hai mẫu mới:", pred)
print("Baseline dùng nhãn train, không biết đáp án của mẫu mới.")
assert pred.tolist() == [0,0]
