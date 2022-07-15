import numpy as np 
import cv2
import math
from ipywidgets import interact, IntSlider , Select
import matplotlib.pyplot as plt
#%matplotlib inline

#0~20
x_volume = 10
y_volume = 10

filename = 'shaun.jpg'
path='src/assets/'
img = cv2.imread(path+filename)
(h, w, c) = img.shape
flex_x = np.zeros((h,w),np.float32)
flex_y = np.zeros((h,w),np.float32)
dst = cv2.remap(img,flex_x,flex_y,cv2.INTER_LINEAR)
for y in range(int(h/2)):
    for x in range(int(w/2)):
        flex_x[y,x] = x + math.sin(x/30) * x_volume
        flex_y[y,x] = y + math.cos(y/30) * y_volume
#h/2* w/2 size
dst = cv2.remap(img,flex_x,flex_y,cv2.INTER_LINEAR)
dst = cv2.cvtColor(dst , cv2.COLOR_BGR2RGB)
new_img = cv2.imread(path+filename)
new_img = cv2.cvtColor(new_img , cv2.COLOR_BGR2RGB)
for y in range(int(h/2)):
    for x in range(int(w/2)):
        new_img[y,x] = dst[y,x]
plt.figure(figsize=(10,10))
plt.tick_params(labelbottom=False,labelleft=False,labelright=False,labeltop=False)
plt.imshow(new_img)
# plt.show()
plt.savefig(path+'shaun_reshape.png')