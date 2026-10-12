# -*- coding: utf-8 -*-
import numpy as np

# Ảnh nhỏ và mask có cùng vị trí đối tượng; flip cả hai cùng nhau.
image=np.array([[10,20,30],[40,50,60]])
mask=np.array([[1,0,0],[1,0,0]])
image_flip=np.fliplr(image); mask_flip=np.fliplr(mask)
print("Image:",image.tolist(),"flipped:",image_flip.tolist())
print("Mask flipped:",mask_flip.tolist())
width=100; x1,x2=10,30
print("Box mới khi flip ngang:",[width-x2,width-x1])
assert np.array_equal(mask_flip,np.array([[0,0,1],[0,0,1]]))
# Mask resize dùng nearest-neighbor; không tạo nhãn trung gian bằng bilinear.
