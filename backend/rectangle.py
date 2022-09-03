# 画像用のモジュール
import cv2
# facemesh用のモジュール
import mediapipe as mp
import math

# 動画を読み込む
#エラー出たらVideoCapture(0)や2とかにしてみる
cap = cv2.VideoCapture(0)
pTime = 0
# モジュールの準備
mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=1)
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=2)

# ビデオの情報
cap_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
cap_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
video_frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT) 
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
#------
  # if(point == 33):
  #   return "右目の左側"
  # if(point == 33):
  #   return "右目の左側"
  # if(point == 33):
  #   return "右目の左側"
  # if(point == 33):
  #   return "右目の左側"
  # righteye=[[zahyo_ue],[zahyo_sita],[zahyo_migi],[zahyo_hidari]]
#------

def judge_right_eye(point):
  return point == 159 or point == 133 or point == 145 or point == 33

#欲しい領域のみ回転させる。切り出しと回転が同時なイメージ。
def rot_cut(src_img, deg, center, size):
    rot_mat = cv2.getRotationMatrix2D(center, deg, 1.0)
    rot_mat[0][2] += -center[0]+size[0]/2 # -(元画像内での中心位置)+(切り抜きたいサイズの中心)
    rot_mat[1][2] += -center[1]+size[1]/2 # 同上
    return cv2.warpAffine(src_img, rot_mat, size)
  
def store_in_right_eye_array(x, y, point, array):
  if(point == 159):
    i = 0
  elif(point == 133):
    i = 1
  elif(point == 145):
    i = 2
  elif(point == 33):
    i = 3
  array[i] = [x, y]
  
def convert_deg(points):
  # 右と左の座標の差をとって傾きの角度を求める
  diff_x = (points[1][0] - points[3][0])
  diff_y = (points[1][1] - points[3][1])
  tilt = diff_y / diff_x
  arctan = math.atan(tilt)
  return math.degrees(arctan)
  
def convert_center(points):
  # 中心の座標を求める
  mid_x = (points[0][0] + points[1][0]) / 2
  mid_y = (points[0][0] + points[1][0]) / 2
  center = [mid_x, mid_y]
  return center

def convert_size(points):
  # 長方形のサイズを求める
  height = math.sqrt((points[0][0] - points[2][0]) * (points[0][0] - points[2][0]) + (points[0][1] - points[2][1]) * (points[0][1] - points[2][1]))
  width = math.sqrt((points[1][0] - points[3][0]) * (points[1][0] - points[3][0]) + (points[1][1] - points[3][1]) * (points[1][1] - points[3][1]))
  size = [height, width]
  return size
  
# 毎フレームこのループが始まる
while True:
    # 点番号用のカウント変数
    cnt = 0
    success, img = cap.read()
    
    right_eye = [0, 0, 0, 0]
    
    if img is None:
        break
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceMesh.process((imgRGB))
    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            # 全部の点を書きたいときはこの一文で十分

            # mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACEMESH_CONTOURS, drawSpec, drawSpec)

            # このループが顔の点分(468)回繰り返される
            # 特定の顔の点を記載したときはこの部分を調整する
            for id, lm in enumerate(faceLms.landmark):
                # 目をプロット
                if judge_right_eye(cnt):
                    # 画像のサイズ取得
                    ih, iw, ic = img.shape
                    # 画像のサイズにfaceLms.landmarkのx,yの値を掛けることで座標になる
                    x, y  = int(lm.x*iw), int(lm.y*ih)
                    # 各パーツの配列に保存
                    store_in_right_eye_array(x, y, cnt, right_eye)
                    # 画像にプロット
                    cv2.drawMarker(img,(x,y),(255,0,0),markerType=cv2.MARKER_STAR,markerSize = 2)
                    
                cnt +=1
                
    cutimg = rot_cut(img, convert_deg(right_eye), convert_center(right_eye), convert_size(right_eye))
            
    # 出力ファイルに記載
    cv2.imshow('MediaPipe FaceMesh', img)
    if cv2.waitKey(5) & 0xFF == 27:
        break
cap.release()