import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from mysql.connector import cursor

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
        self.menu_password.clicked.connect(self.stack_passwd)
        self.menu_register.clicked.connect(self.stack_register)
        self.menu_search.clicked.connect(self.stack_search)
        self.menu_manage.clicked.connect(self.stack_manage)
        self.menu_setting.clicked.connect(self.stack_setting)
        #识别门禁槽函数
        self.menu_index.clicked.connect(self.index_face)
        #用户注册页面槽函数
        self.register_pushButton.clicked.connect(self.save_information)
        self.register_train_pushbuttoon.clicked.connect(self.train_model)
        self.register_video_pushbutton.clicked.connect(self.save_pic)
        #信息管理槽函数
        self.pushButton.clicked.connect(self.manage_delete)
        self.pushButton_2.clicked.connect(self.manage_change)
        self.retinaface = Retinaface()
        openni2.initialize()
        self.dev = openni2.Device.open_any()
        self.color_stream = self.dev.create_color_stream()
        self.color_stream.start()
        self.painter = QPainter(self)


    def stack_index(self):
        self.stackedWidget.setCurrentIndex(0)
    def stack_passwd(self):
        self.stackedWidget.setCurrentIndex(1)
    def stack_register(self):
        self.stackedWidget.setCurrentIndex(2)
    def stack_search(self):
        self.stackedWidget.setCurrentIndex(3)
    def stack_manage(self):
        self.stackedWidget.setCurrentIndex(4)
    def stack_setting(self):
        self.stackedWidget.setCurrentIndex(5)
   #####################################################
   #################人脸识别界面##########################
    def index_face(self):
        mycursor = config.mydb.cursor()
        try:
            # 执行SQL语句
            mycursor.execute("select * from student where id = '%s'" % (Retinaface.name))
            # 获取所有记录列表
            results = mycursor.fetchall()
            for row in results:
                self.index_input_id.setPlaceholderText(row[0])
                self.index_input_name.setPlaceholderText(row[1])
                self.index_input_work.setPlaceholderText(row[2])
                self.index_input_tel.setPlaceholderText(row[3])
                id = row[0]
        except:
            print("Error: unable to fetch data")




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
    def train_model(self):
        # 将所有人脸编码的结果放在一个列表中，得到的就是已知的所有人脸的特征列表，在之后获得的实时图片中的人脸都需要与已知的列表进行对比，就能知道谁是谁
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

        #############################################################
        ##################### 信息管理 ###############################
    def manage_delete(self):
        mycursor = config.mydb.cursor()
        id = self.manage_input_id.text()
        mycursor.execute("delete from student where id = '%s'" % id)
        # 提交语句
        config.mydb.commit()
    def manage_change(self):
        mycursor = config.mydb.cursor()
        # id = self.manage_input_id_2.text()
        # sql = "INSERT INTO student (id, name, work, tel) VALUES (%s, %s, %s, %s)"
        #
        # mycursor.execute("update student set (name=%s , work=%s, tel=%s) where id=%s", [, 5, ])
        # mycursor.commit()
        mycursor.execute("update student set name=%s , work=%s, tel=%s where id=%s", [self.register_input_name.text(), self.register_input_work.text(),
               self.register_input_tel.text(),self.register_input_id.text()])
        # sql = "update student set (name, work, tel) where id VALUES (%s, %s, %s, %s)"
        # val = (self.register_input_name.text(), self.register_input_work.text(),
        #        self.register_input_tel.text(),self.register_input_id.text(), )
        # mycursor.execute(sql, val)
        config.mydb.commit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = myMainWindow()
    ui.show()
    sys.exit(app.exec_())
