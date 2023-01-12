import cv2 as cv

def face_detect_demo(img):
    gary =cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    face_detect = cv.CascadeClassifier(cv.data.haarcascades+'/haarcascade_frontalface_alt2.xml')
    face =face_detect.detectMultiScale(gary, 1.1, 5,)  #1.1每次缩放的倍数，5遍历五次都有人脸确定有
    for x, y, w, h in face:
        cv.rectangle(img, (x, y), (x+w, y+h), color=(0,0,255), thickness=2)
    cv.imshow('result', img)

#读取摄像头
cap =cv.VideoCapture(0)

#读取视频
#cap = cv.VideoCapture('1.mp4')

#等待
while True:
    flag, frame = cap.read()
    if not flag:
        break
    face_detect_demo(frame)
    if ord('q') == cv.waitKey(0):
        break
#释放内存
cv.destoryAllWindows()
#释放摄像头
cap.release()