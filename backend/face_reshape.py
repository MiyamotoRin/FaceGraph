import numpy as np 
import pandas as pd 
import cv2
import math
import matplotlib.pyplot as plt
#%matplotlib inline
#csvを読み込む
import deal_csv

#データの読み込み，正規化
csv_file = '.csv'
#pd.dataframe, コラム名，インデックスを返す
#data[i][j]の大きさがゆがみパラメータ
data, columns, indexs = deal_csv.deal_csv(csv_file)

#画像Path
img_file = 'shaun.jpg'
path='src/assets/'
img = cv2.imread(path+img_file)
(h, w, c) = img.shape

#顔メッシュ生成 pipeline


#矩形を切り出す，パーツごとの画像arrを生成
flex_x = np.zeros((h,w),np.float32)
flex_y = np.zeros((h,w),np.float32)
dst = cv2.remap(img,flex_x,flex_y,cv2.INTER_LINEAR)


#indexsの数だけ画像を生成
for index in indexs:
    
    
    #indexに関したcolumns（属性）の数だけ，dataの値に応じてパーツを歪ませる
    for column in  columns:

        for y in range(int(h/2)):
            for x in range(int(w/2)):
                #パラメタ x_volume=data[column][index]という感じになる
                volume=data[column][index]
                flex_x[y,x] = x + math.sin(x/30) * volume
                flex_y[y,x] = y + math.cos(y/30) * y_volume
        #h/2* w/2 size
        dst = cv2.remap(img,flex_x,flex_y,cv2.INTER_LINEAR)
        dst = cv2.cvtColor(dst , cv2.COLOR_BGR2RGB)

    #歪ませたパーツをくっつける
    #保存用画像
    new_img = cv2.imread(path+img_file)
    new_img = cv2.cvtColor(new_img , cv2.COLOR_BGR2RGB)
    for column in  columns:
        for y in range(int(h/2)):
            for x in range(int(w/2)):
                new_img[y,x] = dst[y,x]

    #保存
    cv2.imwrite(path+img_file+index+'_graph.png', new_img)