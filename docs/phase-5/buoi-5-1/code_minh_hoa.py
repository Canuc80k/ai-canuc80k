# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

texts=["rain floods city","storm damages bridge","team wins match", "player scores goal"]
y=[1,1,0,0]  # Fixture: 1 thời tiết, 0 thể thao.
model=make_pipeline(TfidfVectorizer(),LogisticRegression(random_state=42))
model.fit(texts,y)
print("Vocabulary:",sorted(model[0].vocabulary_))
query=["rain storm","team player"]
print("Labels:",model.predict(query).tolist())
print("Probs:",model.predict_proba(query).round(4).tolist())
assert model.predict(query).tolist()==[1,0]
# Fit vocabulary/IDF chỉ trên train; fixture ít câu chỉ để đọc thao tác.
