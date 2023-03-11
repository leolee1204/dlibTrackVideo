import cv2
import dlib

def track_video(readVideoName,writeVideoName):
    video = cv2.VideoCapture(readVideoName)
    ret, frame = video.read()

    #selectROI
    bbox = cv2.selectROI(frame)
    cv2.destroyAllWindows()

    (x1, y1, w, h) = bbox
    x2 = x1 + w
    y2 = y1 + h
    #dlib四點座標
    dlibRect = dlib.rectangle(x1, y1, x2, y2)

    #dlib need RGB
    rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    #初始化，並啟動tracker
    tracker = dlib.correlation_tracker()
    tracker.start_track(rgb, dlibRect)

    trackX1 = trackY1 = trackX2 = trackY2 = 0

    #write video
    frame_w,frame_h,c = frame.shape
    fps = video.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    output = cv2.VideoWriter(writeVideoName, fourcc, 20.0, (frame_h,frame_w))

    #從第一偵開始 第四偵檢查
    frame_index = 1+3
    while True:
        frame_index_start = video.get(cv2.CAP_PROP_POS_FRAMES)

        ret, frame = video.read()
        if ret == False:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 看新的一幀，繼續track
        tracker.update(rgb)

        # 獲得追蹤物件的新位址
        objectPosition = tracker.get_position()

        x1 = int(objectPosition.left())
        y1 = int(objectPosition.top())
        x2 = int(objectPosition.right())
        y2 = int(objectPosition.bottom())

        if (x1,y1,x2,y2) == (trackX1,trackY1,trackX2,trackY2):
            text = "Object not move"
            color = (0, 0, 255)
        else:
            text = 'tracking'
            color = (0, 255, 0)

        #每三偵檢查一次，查看座標是否移動
        if frame_index_start == frame_index:
            (trackX1,trackY1,trackX2,trackY2) = (x1,y1,x2,y2)
            frame_index = frame_index_start+3

        cv2.putText(frame, text, (20, 70),cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)

        cv2.imshow("Tracker", frame)
        output.write(frame)

        k = cv2.waitKey(5)
        if k == 27:
            break

    video.release()
    cv2.destroyAllWindows()
