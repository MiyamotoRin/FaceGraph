import numpy as np 
import pandas as pd 
import cv2
import math
import io
from PIL import Image
import sys
import base64
import json
#csvを読み込む
import deal_csv

def distorter(img, x_volume, y_volume):
    (h, w, c) = img.shape
    right_edge = w
    left_edge = 0
    top_edge = 0
    bottom_edge = h

    flex_x = np.zeros((bottom_edge,right_edge),np.float32)
    flex_y = np.zeros((bottom_edge,right_edge),np.float32)
    dst = cv2.remap(img,flex_x,flex_y,cv2.INTER_LINEAR)
    for y in range(top_edge,bottom_edge):
        for x in range(left_edge,right_edge):
            flex_x[y,x] = x + math.sin(x/30) * x_volume
            flex_y[y,x] = y + math.cos(y/30) * y_volume
    dst = cv2.remap(img,flex_x,flex_y,cv2.INTER_LINEAR)
    dst = cv2.cvtColor(dst , cv2.COLOR_BGR2RGB)
    return dst


#データの読み込み，正規化
csv_file = '.csv'
#pd.dataframe, コラム名，インデックスを返す
#data[i][j]の大きさがゆがみパラメータ
data, columns, indexs = deal_csv.deal_csv(csv_file)

#画像Path
data = sys.argv
img = cv2.imread(data[1])
new_img= img.copy()
(h, w, c) = img.shape
#顔メッシュ生成 pipeline


#矩形を切り出す，パーツごとの画像arrを生成


#indexsの数だけ画像を生成
for index in indexs:
    #indexに関したcolumns（属性）の数だけ，dataの値に応じてパーツを歪ませる
    len_half = int(len(columns)/2)
    for i in  range(len_half):
        dst = distorter(parts_img[i], 
                        x_volume=data[columns[2*i]][index],
                        y_volume=data[columns[2*i+1]][index]
                        )
        #columnsの数が2で割り切れないときはx軸方向のみ歪ませる
        if(i == len_half-1 and len_half*2 < len(columns) ):
            dst = distorter(parts_img[i+1], 
                            x_volume=data[columns[2*i]][index],
                            y_volume=0.0
                            )


    #歪ませたパーツをくっつける
    #保存用画像
    new_img = cv2.imread(path+img_file)
    new_img = cv2.cvtColor(new_img , cv2.COLOR_BGR2RGB)
    for column in  columns:
        #各部位の4点座標を持った配列の格納順は[左上,右上,左下,右下]を想定
        #右目 right_eye_plot
        #if right_eye_el != 0
        for y in range(right_eye_plot[2][1]-right_eye_plot[0][1]):
            for x in range(int(right_eye_plot[1][0]-right_eye_plot[0][0])):
                new_img[y+right_eye_plot[0][1],x+right_eye_plot[0][0]] = dst[y+right_eye_plot[0][1],x+right_eye_plot[0][0]]

        #左目 right_eye_plot
        #if left_eye_el!=0:
        for y in range(left_eye_plot[2][1]-left_eye_plot[0][1]):
            for x in range(int(left_eye_plot[1][0]-left_eye_plot[0][0])):
                new_img[y+left_eye_plot[0][1],x+left_eye_plot[0][0]] = dst[y+left_eye_plot[0][1],x+left_eye_plot[0][0]]

        #鼻 nose_plot
        #if nose_el != 0:
        for y in range(nose_plot[2][1]-nose_plot[0][1]):
            for x in range(int(nose_plot[1][0]-nose_plot[0][0])):
                new_img[y+nose_plot[0][1],x+nose_plot[0][0]] = dst[y+nose_plot[0][1],x+nose_plot[0][0]]

        #口 mouth_plot
        #if mouth_el!= 0:
            for y in range(mouth_plot[2][1]-mouth_plot[0][1]):
                for x in range(int(mouth_plot[1][0]-mouth_plot[0][0])):
                    new_img[y+mouth_plot[0][1],x+mouth_plot[0][0]] = dst[y+mouth_plot[0][1],x+mouth_plot[0][0]]
                    
                # for y in range(int(h/2)):
                #     for x in range(int(w/2)):
                #         new_img[y,x] = dst[y,x]




    #境界ぼかし
    #cp_img = new_img.copy()
    #左辺,右辺
    #int(w/4),int(3*w/4)-1などは矩形の端の座標
    #左辺,右辺
    right_edge = int(3*w/4)
    left_edge = int(w/4)
    top_edge = int(h/4)
    bottom_edge = int(3*h/4)
    for x in [left_edge,right_edge]:
        #画像の両端でない場合
        for i in [-2,-1,0,1,2]:
            for y in range(top_edge,bottom_edge):
                if(x-4>0 and x+4 < w and y-2>0 and y+2 < h):
                    new_img[y,x] = (cp_img[y-2+i,x-2+i] / 25 +cp_img[y-2+i,x-1+i] / 25 + cp_img[y-2+i,x+i] / 25 + cp_img[y-2+i,x+1+i] / 25 +cp_img[y-2+i,x+2+i] / 25+
                                cp_img[y-1+i,x-2+i] / 25 +cp_img[y-1+i,x-1+i] / 25 + cp_img[y-1+i,x+i] / 25 + cp_img[y-1+i,x+1+i] / 25 +cp_img[y-1+i,x+2+i] / 25+
                                cp_img[y+i,x-2+i] / 25 + cp_img[y+i,x-1+i] / 25 + cp_img[y+i,x+i] / 25 + cp_img[y+i,x+1+i] / 25 + cp_img[y+i,x+2+i] / 25 +
                                cp_img[y+1+i,x-2+i] / 25 + cp_img[y+1+i,x-1+i] / 25 + cp_img[y+1+i,x+i] / 25 + cp_img[y+1+i,x+1+i] / 25 + cp_img[y+1+i,x+2+i] / 25+
                                cp_img[y+2+i,x-2+i] / 25 + cp_img[y+2+i,x-1+i] / 25 + cp_img[y+2+i,x+i] / 25 + cp_img[y+2+i,x+1+i] / 25 + cp_img[y+2+i,x+2+i] / 25
                                )
        
    #上底,下底
    for y in [int(h/4),int(3*h/4)-1]:
        for i in [-2,-1,0,1,2]:
            for x in range(int(w/4),int(3*w/4)):
                if(x-2>0 and x+2 < w and y-4>0 and y+4 < h):
                    new_img[y,x] = (cp_img[y-2+i,x-2+i] / 25 +cp_img[y-2+i,x-1+i] / 25 + cp_img[y-2+i,x+i] / 25 + cp_img[y-2+i,x+1+i] / 25 +cp_img[y-2+i,x+2+i] / 25+
                                cp_img[y-1+i,x-2+i] / 25 +cp_img[y-1+i,x-1+i] / 25 + cp_img[y-1+i,x+i] / 25 + cp_img[y-1+i,x+1+i] / 25 +cp_img[y-1+i,x+2+i] / 25+
                                cp_img[y+i,x-2+i] / 25 + cp_img[y+i,x-1+i] / 25 + cp_img[y+i,x+i] / 25 + cp_img[y+i,x+1+i] / 25 + cp_img[y+i,x+2+i] / 25 +
                                cp_img[y+1+i,x-2+i] / 25 + cp_img[y+1+i,x-1+i] / 25 + cp_img[y+1+i,x+i] / 25 + cp_img[y+1+i,x+1+i] / 25 + cp_img[y+1+i,x+2+i] / 25+
                                cp_img[y+2+i,x-2+i] / 25 + cp_img[y+2+i,x-1+i] / 25 + cp_img[y+2+i,x+i] / 25 + cp_img[y+2+i,x+1+i] / 25 + cp_img[y+2+i,x+2+i] / 25
                                )

    #保存
    pil_img = Image.fromarray(new_img)
    output = io.BytesIO()
    pil_img.save(output, format='PNG')
    img_png = output.getvalue()
    o_img_b64 = base64.b64encode(img_png).decode('utf-8')
    img_header = 'data:image/png;base64,'
    result = {'resultImages':[img_header+o_img_b64]}
    print(json.dumps(result))