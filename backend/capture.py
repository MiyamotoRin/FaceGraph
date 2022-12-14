# 画像用のモジュール
import cv2
# facemesh用のモジュール
import mediapipe as mp
# パスを入力
video_file = "分析したい動画の絶対パス"
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

# 出力ファイル
#writer = cv2.VideoWriter("出力パス",fourcc, fps, (cap_width, cap_height))

# 毎フレームこのループが始まる
while True:
    # 点番号用のカウント変数
    cnt = 0
    success, img = cap.read()
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
                # 今回の場合は点番号10, 0 , 152, 264のみをプロット
                if cnt == 10 or cnt == 0 or cnt == 152 or cnt == 264 :
                    # 画像のサイズ取得
                    ih, iw, ic = img.shape
                    # 画像のサイズにfaceLms.landmarkのx,yの値を掛けることで座標になる
                    x, y  = int(lm.x*iw), int(lm.y*ih)
                    # 画像にプロット
                    cv2.drawMarker(img,(x,y),(255,0,0),markerType=cv2.MARKER_STAR,markerSize = 2)
                cnt +=1
    # 出力ファイルに記載
    cv2.imshow('MediaPipe FaceMesh', img)
    if cv2.waitKey(5) & 0xFF == 27:
        break
cap.release()