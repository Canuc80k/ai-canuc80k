# -*- coding: utf-8 -*-

# Ký tự cuối mỗi từ con được đánh dấu 1; indices theo ký tự Unicode.
word="rainbow"; labels=[0,0,0,1,0,0,1]
def spans(word,labels):
    if len(word)!=len(labels) or not labels or labels[-1]!=1:
        raise ValueError("Sai chiều dài hoặc thiếu ranh giới cuối")
    start=0; result=[]
    for end,label in enumerate(labels):
        if label==1: result.append((start,end+1,word[start:end+1])); start=end+1
    return result
print("Spans:",spans(word,labels))
print("Số ký tự tiếng Việt:",len("học"),"số bytes UTF8:",len("học".encode("utf-8")))
assert [s[2] for s in spans(word,labels)]==["rain","bow"]
