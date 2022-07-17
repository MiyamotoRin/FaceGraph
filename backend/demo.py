import numpy as np 
import cv2
import math
import matplotlib.pyplot as plt
import io
from PIL import Image
import sys
import base64
import json

#0~20
x_volume = 10
y_volume = 10

data = sys.argv
img = cv2.imread(data[1])
new_img = img.copy()

(h, w, c) = img.shape
flex_x = np.zeros((h,w),np.float32)
flex_y = np.zeros((h,w),np.float32)
dst = cv2.remap(img,flex_x,flex_y,cv2.INTER_LINEAR)
for y in range(int(h/2)):
    for x in range(int(w/2)):
        flex_x[y,x] = x + math.sin(x/30) * x_volume
        flex_y[y,x] = y + math.cos(y/30) * y_volume

dst = cv2.remap(img,flex_x,flex_y,cv2.INTER_LINEAR)
dst = cv2.cvtColor(dst , cv2.COLOR_BGR2RGB)
new_img = cv2.cvtColor(new_img , cv2.COLOR_BGR2RGB)
for y in range(int(h/2)):
    for x in range(int(w/2)):
        new_img[y,x] = dst[y,x]

pil_img = Image.fromarray(new_img)
output = io.BytesIO()
pil_img.save(output, format='PNG')
img_png = output.getvalue()
o_img_b64 = base64.b64encode(img_png).decode('utf-8')
img_header = 'data:image/png;base64,'
res = img_header+o_img_b64
result = {'resultImages':[res, res, res]}

print(json.dumps(result))