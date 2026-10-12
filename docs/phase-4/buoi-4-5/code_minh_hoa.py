# -*- coding: utf-8 -*-

def iou(a,b):
    x1=max(a[0],b[0]); y1=max(a[1],b[1])
    x2=min(a[2],b[2]); y2=min(a[3],b[3])
    intersection=max(0,x2-x1)*max(0,y2-y1)
    area_a=(a[2]-a[0])*(a[3]-a[1])
    area_b=(b[2]-b[0])*(b[3]-b[1])
    return intersection/(area_a+area_b-intersection)
A=[0,0,2,2]; B=[1,1,3,3]
print("IoU:",round(iou(A,B),6))
boxes=[(0,.9,A),(1,.8,B),(2,.7,[5,5,7,7])]
kept=[]
for ident,score,box in sorted(boxes,key=lambda row:(-row[1],row[0])):
    if all(iou(box,previous[2])<=.1 for previous in kept): kept.append((ident,score,box))
print("NMS giữ IDs:",[row[0] for row in kept])
assert [row[0] for row in kept]==[0,2]
