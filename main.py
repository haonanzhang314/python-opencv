import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimediaWidgets import QVideoWidget
from register import Ui_MainWindow
import sys
import time
import cv2
import numpy as np
from openni import openni2
import utils.config as config
from retinaface import Retinaface



class myMainWindow(Ui_MainWindow,QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.save_information)


   # 保存相应数据到数据库
    def save_information(self):



        mycursor = config.mydb.cursor()
        sql = "INSERT INTO student (id, name, telephone, password, class) VALUES (%s, %s, %s, %s, %s)"
        val = (self.id.text(), self.name.text(), self.name.text(), self.tellphone.text(), self.classes.text())
        mycursor.execute(sql, val)
        config.mydb.commit()

        retinaface = Retinaface()




        openni2.initialize()

        dev = openni2.Device.open_any()
        # 打印设备型号
        print(dev.get_device_info())
        # 彩色通道
        color_stream = dev.create_color_stream()

        color_stream.start()
        i = 0;

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
            cframe_data = np.array(retinaface.detect_image(cframe_data))

            fps = (fps + (1. / (time.time() - t1))) / 2
            print("fps= %.2f" % (fps))

            cframe_data = cv2.putText(cframe_data, "fps= %.2f" % (fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                      (0, 255, 0),
                                      2)

            # cv2.imshow("video", cframe_data)
            cframe_data = PyQt5.QtGui.QPixmap(cframe_data).scaled(self.video.width(),self.video.height())

            self.label.setPixmap(cframe_data)

            # waitkey(0)表示函数无限长，waitkey（1）表示每1ms检查一次按键
            c = cv2.waitKey(1) & 0xff
            if c == ord('s'):
                i += 1
                name = id
                cv2.imencode('.jpg', cframe_data)[1].tofile('face_dataset/' + name + '_' + str(i) + '.jpg')
                print(i)

            # 如果有esc（esc的ASCII为27）键按下，退出循环（break）
            if c == 27:
                color_stream.stop()
                break
        print("Video Detection Done!")


















if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = myMainWindow()
    ui.show()
    sys.exit(app.exec_())
