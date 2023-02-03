import cv2 as cv
import os
import numpy as np
from PIL import Image
import urllib
import urllib.request

# 加载训练数据集文件
recognizer = cv.face.LBPHFaceRecognizer_create()
# 加载数据
recognizer.read('trainer/trainer.yml')
# 名字
names = []
# 警报全局变量
warningtime = 0

face_detector = cv.CascadeClassifier(cv.data.haarcascades + '/haarcascade_frontalface_alt2.xml')

# 准备识别的图像
def face_detect_demo(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # 转换为灰度
    # 加载官方人脸识别器

    face_detector = cv.CascadeClassifier(cv.data.haarcascades + '/haarcascade_frontalface_alt2.xml')

    # 在gray图上找出人脸
    face = face_detector.detectMultiScale(gray, 1.01, 5, cv.CASCADE_SCALE_IMAGE, (180, 180), (300, 300))

    for x, y, w, h in face:
        # 在img上面绘制脸部方框
        cv.rectangle(img, (x, y), (x + w, y + h), color=(0, 0, 255), thickness=1)
        # img上绘制脸部圆圈
        cv.circle(img, center=(x + w // 2, y + h // 2), radius=w // 2, color=(0, 255, 0), thickness=1)
        # 人脸识别

        ids, confidence = recognizer.predict(gray[y:y + h, x:x + w])
        print(ids)
        print('confidence:', confidence)
        print('name:', names[ids - 1])

        if confidence > 120:
            # gloal声明一个全局变量
            global warningtime
            warningtime += 1

            if warningtime > 100:
                # 不是存储在数据库中的人脸，图片上打印：unknown
                #
                #
                cv.putText(img, 'unknown', (x, y + 15), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 1)

        else:
            cv.putText(img, str(names[ids - 1]), (x, y + 15), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 1)

    cv.imshow('result', img)


def name():
    imagePaths = []

    path = '/home/haonan/PycharmProjects/python-opencv/img/'

    for file in os.listdir(path):

        if file.endswith('jpg'):
            # 路径拼接，imagePath是图片的绝对路径
            imagePath = os.path.join(path, file)
            # 将图片路径添加到列表中
            imagePaths.append(imagePath)
    # 得到图片文件名中的名字
    for imagePath in imagePaths:
        # 打开图片，灰度化PIL有九种不同模式，其中1为黑白，L为灰度
        PIL_img = Image.open(imagePath).convert('L')
        # 将图像转换成数组，以黑白深浅
        img_numpy = np.array(PIL_img, 'uint8')
        # 获取图片人脸特征
        faces = face_detector.detectMultiScale(image=img_numpy, scaleFactor=1.01, minNeighbors=5, minSize=(180, 180),
                                               maxSize=(300, 300))
        # 得到图片绝对路径列表中的人名，存储在names列表

        name = (os.path.split(imagePath)[1].split('.')[1]).split('.')[0]

        # 预防无面容照片
        for x, y, w, h in faces:
            names.append(name)

            # 打印脸部特征和id
            print('id:', id)
            print('name:', name)
            print('fs', img_numpy[y:y + h, x:x + w])
    print(names)


cap = cv.VideoCapture(0)
name()

# #以图片做实验
# #D:\SoftwareCache\PyCharmCache\Project_Face\trainer\FERET_80_80\FERET_80_80-人脸数据库\FERET-001-Lesley
#
# frame = cv.imread('./face8.jpg')
# face_detect_demo(frame)
#
# while True:
#     if ord('q') == cv.waitKey(0):
#         break
#
# cv.destroyAllWindows()


# 以摄像头捕捉图像做实验
while True:
    flag, frame = cap.read()
    if not flag:
        break
    face_detect_demo(frame)

    if ord(' ') == cv.waitKey(10):
        break

cv.destroyAllWindows()
cap.release()

