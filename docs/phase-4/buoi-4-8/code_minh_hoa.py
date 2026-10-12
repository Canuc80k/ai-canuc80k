# -*- coding: utf-8 -*-
import numpy as np

# Gallery embeddings và IDs cố định; query chưa có nhãn.
gallery=np.array([[1.,0.],[0.,1.],[1.,1.]])
ids=np.array([10,20,30]); query=np.array([.9,.1])
gallery=gallery/np.linalg.norm(gallery,axis=1,keepdims=True)
query=query/np.linalg.norm(query)
scores=gallery@query
order=np.lexsort((ids,-scores))
print("Scores:",scores.round(4).tolist())
print("Ranking IDs:",ids[order].tolist())
assert ids[order].tolist()==[10,30,20]
# CLIP là một cách tạo embeddings thật; file clip_demo.py chỉ dùng model đã cấp/cache.
