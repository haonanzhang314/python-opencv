import os
from retinaface import Retinaface

import time
import cv2
import numpy as np
from openni import openni2

import mysql.connector

mydb = mysql.connector.connect(
  host="124.221.206.185",
  user="face",
  passwd="qwe123ASD",
  database='face'
)
if __name__ == "__main__":
    id = input("请输入你的学号或工号")
    i = 0
    name = input("请输入你的名字")
    telephone = input("请输入你的联系方式")
    password = input("请设定密码")
    classes = input("请输入班级")
    mycursor = mydb.cursor()
    sql = "INSERT INTO student (id, name, telephone, password, class) VALUES (%s, %s, %s, %s, %s)"
    val = (id, name, telephone, password, classes)
    mycursor.execute(sql, val)
    mydb.commit()
    print("1 record inserted, ID:", mycursor.lastrowid)



    openni2.initialize()

    dev = openni2.Device.open_any()
    # 打印设备型号
    print(dev.get_device_info())
    # 彩色通道
    color_stream = dev.create_color_stream()

    color_stream.start()

    fps = 0.0

    while (True):

        t1 = time.time()

        cframe = color_stream.read_frame()

        cframe_data = np.array(cframe.get_buffer_as_triplet()).reshape([480, 640, 3])
        R = cframe_data[:, :, 0]
        G = cframe_data[:, :, 1]
        B = cframe_data[:, :, 2]
        cframe_data = np.transpose(np.array([B, G, R]), [1, 2, 0])

        # 进行检测
        # cframe_data = np.array(retinaface.detect_image(cframe_data))

        fps = (fps + (1. / (time.time() - t1))) / 2
        print("fps= %.2f" % (fps))

        cframe_data = cv2.putText(cframe_data, "fps= %.2f" % (fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                                  2)

        cv2.imshow("video", cframe_data)

        # waitkey(0)表示函数无限长，waitkey（1）表示每1ms检查一次按键
        c = cv2.waitKey(1) & 0xff
        if c == ord('s'):
            i += 1
            name = id
            cv2.imencode('.jpg', cframe_data)[1].tofile('face_dataset/'+name+'_'+str(i)+'.jpg')
            print(i)


        # 如果有esc（esc的ASCII为27）键按下，退出循环（break）
        if c == 27:
            color_stream.stop()
            break
    print("Video Detection Done!")

    cv2.destroyAllWindows()

    import os

    from retinaface import Retinaface

    '''
    在更换facenet网络后一定要重新进行人脸编码，运行encoding.py。
    '''
    retinaface = Retinaface(1)

    list_dir = os.listdir("face_dataset")
    image_paths = []
    names = []
    for name in list_dir:
        image_paths.append("face_dataset/" + name)
        names.append(name.split("_")[0])

    retinaface.encode_face_dataset(image_paths, names)





