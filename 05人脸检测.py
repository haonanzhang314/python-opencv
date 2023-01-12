import cv2 as cv

def face_detect_demo():
    gary =cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    face_detect = cv.CascadeClassifier(cv.data.haarcascades+'/haarcascade_frontalface_alt2.xml')
    face =face_detect.detectMultiScale(gary, 1.1, 5,)  #1.1每次缩放的倍数，5遍历五次都有人脸确定有
    for x, y, w, h in face:
        cv.rectangle(img, (x, y), (x+w, y+h), color=(0,0,255), thickness=2)
    cv.imshow('result', img)
#读取图片
img = cv.imread('data/001.jpg')
#检测函数
face_detect_demo()

#等待
while True:
    if ord('q') == cv.waitKey(0):
        break
#释放内存
cv.destoryAllWindows()