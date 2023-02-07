import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from mainwindow import Ui_MainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui
import cv2
import time
import utils.config as config
import numpy as np
from openni import openni2
from retinaface import Retinaface



class myMainWindow(Ui_MainWindow,QMainWindow):
    i = 0
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        #实现页面跳转
        self.menu_index.clicked.connect(self.stack_index)
        self.menu_register.clicked.connect(self.stack_register)
        self.menu_search.clicked.connect(self.stack_serch)
        #识别门禁槽函数
        self.menu_index.clicked.connect(self.index_face)
        #用户注册页面槽函数
        self.register_pushButton.clicked.connect(self.save_information)
        self.register_video_pushbutton.clicked.connect(self.save_pic)
        self.retinaface = Retinaface()
        openni2.initialize()
        self.dev = openni2.Device.open_any()
        self.color_stream = self.dev.create_color_stream()
        self.color_stream.start()
        self.painter = QPainter(self)

    def stack_index(self):
        self.stackedWidget.setCurrentIndex(0)
    def stack_register(self):
        self.stackedWidget.setCurrentIndex(1)
    def stack_serch(self):
        self.stackedWidget.setCurrentIndex(2)
   #####################################################
   #################人脸识别界面##########################
    def index_face(self):
        mycursor = config.mydb.cursor()
        mycursor.execute("select * from student where id = '%s'" % (Retinaface.name))
        for x in mycursor:
            print(x)



   #####################################################
   #################用户注册模块##########################
   # 保存相应数据到数据库
    def save_information(self):
        print(self.index_input_id.text())

        mycursor = config.mydb.cursor()
        sql = "INSERT INTO student (id, name, work, tel) VALUES (%s, %s, %s, %s)"
        val = (self.register_input_id.text(), self.register_input_name.text(), self.register_input_work.text(), self.register_input_tel.text())
        mycursor.execute(sql, val)
        config.mydb.commit()

    def paintEvent(self, a0: QtGui.QPaintEvent):
        t1 = time.time()
        fps = 0.0
        i = 0

        cframe = self.color_stream.read_frame()
        cframe_data = np.array(cframe.get_buffer_as_triplet()).reshape([480, 640, 3])
        R = cframe_data[:, :, 0]
        G = cframe_data[:, :, 1]
        B = cframe_data[:, :, 2]
        #此处图像无预测框等信息
        self.frame_data = np.transpose(np.array([B, G, R]), [1, 2, 0])
        cframe_data = np.array(self.retinaface.detect_image(self.frame_data))
        fps = (fps + (1. / (time.time() - t1))) / 2
        cframe_data = cv2.putText(cframe_data, "fps= %.2f" % (fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                                   2)

        self.Qframe = QImage(cframe_data.data.tobytes(), cframe_data.shape[1], cframe_data.shape[0], cframe_data.shape[1] * 3,
                             QImage.Format_RGB888)
        self.register_video.setPixmap(QPixmap.fromImage(self.Qframe))
        self.index_video.setPixmap(QPixmap.fromImage(self.Qframe))
        self.update()
    def save_pic(self):
        myMainWindow.i += 1
        name = self.register_input_id.text()
        print(name)
        cv2.imencode('.jpg', self.frame_data)[1].tofile('face_dataset/' + name + '_' + str(myMainWindow.i) + '.jpg')
        print(myMainWindow.i)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = myMainWindow()
    ui.show()
    sys.exit(app.exec_())
