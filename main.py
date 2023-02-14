import os
import sys
import cv2
import time
from time import sleep
import numpy as np
from openni import openni2
import utils.config as config
from retinaface import Retinaface
from mainwindow import Ui_MainWindow
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui





class myMainWindow(Ui_MainWindow,QMainWindow):
    i = 0
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        # 实现页面跳转
        self.menu_index.clicked.connect(self.stack_index)
        self.menu_password.clicked.connect(self.stack_passwd)
        self.menu_register.clicked.connect(self.stack_register)
        self.menu_search.clicked.connect(self.stack_search)
        self.menu_manage.clicked.connect(self.stack_manage)
        self.menu_setting.clicked.connect(self.stack_setting)
        # 识别门禁槽函数
        #self.menu_index.clicked.connect(self.index_face)
        # 密码解锁槽函数
        self.password_pushButton_0.clicked.connect(self.pb00)
        self.password_pushButton_1.clicked.connect(self.pb01)
        self.password_pushButton_2.clicked.connect(self.pb02)
        self.password_pushButton_3.clicked.connect(self.pb03)
        self.password_pushButton_4.clicked.connect(self.pb04)
        self.password_pushButton_5.clicked.connect(self.pb05)
        self.password_pushButton_6.clicked.connect(self.pb06)
        self.password_pushButton_7.clicked.connect(self.pb07)
        self.password_pushButton_8.clicked.connect(self.pb08)
        self.password_pushButton_9.clicked.connect(self.pb09)
        self.password_pushButton_enter.clicked.connect(self.pbenter)
        # 搜索槽函数
        self.search_pushButton.clicked.connect(self.infromation_search)
        # 用户注册页面槽函数
        self.register_pushButton.clicked.connect(self.save_information)
        self.register_train_pushbuttoon.clicked.connect(self.train_model)
        self.register_video_pushbutton.clicked.connect(self.save_pic)
        # 信息管理槽函数
        self.pushButton.clicked.connect(self.manage_delete)
        self.pushButton_2.clicked.connect(self.manage_change)
        # astra相机以及retinaface相关
        openni2.initialize()
        self.retinaface = Retinaface()
        self.dev = openni2.Device.open_any()
        self.color_stream = self.dev.create_color_stream()
        self.color_stream.start()
        self.painter = QPainter(self)

    # 实现菜单栏跳转
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


    # 密码解锁
    def pb00(self):
        self.password_lineEdit_passwd.insert('0')
    def pb01(self):
        self.password_lineEdit_passwd.insert('1')
    def pb02(self):
        self.password_lineEdit_passwd.insert('2')
    def pb03(self):
        self.password_lineEdit_passwd.insert('3')
    def pb04(self):
        self.password_lineEdit_passwd.insert('4')
    def pb05(self):
        self.password_lineEdit_passwd.insert('5')
    def pb06(self):
        self.password_lineEdit_passwd.insert('6')
    def pb07(self):
        self.password_lineEdit_passwd.insert('7')
    def pb08(self):
        self.password_lineEdit_passwd.insert('8')
    def pb09(self):
        self.password_lineEdit_passwd.insert('9')
        # 在按下确认键后将执行下面操作
    def pbenter(self):
        exp = self.password_lineEdit_passwd.text()
        self.password_lineEdit_passwd.clear()
        mycursor = config.mydb.cursor()
        # 执行SQL语句
        mycursor.execute("select * from student where passwd = '%s'" % (exp))
        # 获取所有记录列表
        #results = mycursor.fetchall()
        results = mycursor
        print(results)
        if results != []:
            print("通过密码开锁成功,请通过！")
        else:
            print("密码输入错误，请重新输入!")
    #
    def infromation_search(self):
        exp = self.search_lineEdit_input.text()
        mycursor = config.mydb.cursor()
        # 执行SQL语句
        mycursor.execute("select * from student where id = '%s'" % (exp))
        results = mycursor.fetchall()
        print(results)

    # 人脸识别界面
    def update(self):
        name = Retinaface.name
        self.index_face()
        #if name != "Unknown":

    def index_face(self):

        mycursor = config.mydb.cursor()
        try:
            # 执行SQL语句
            mycursor.execute("select * from student where id = '%s'" % (Retinaface.name))
            # 获取所有记录列表
           # results = mycursor.fetchall()
            for row in mycursor:
                self.index_input_id.setText(row[0])
                self.index_input_name.setText(row[1])
                self.index_input_work.setText(row[2])
                self.index_input_tel.setText(row[3])
                id = row[0]
                sleep(3)

        except:
            print("Error: unable to fetch data")







   # 用户注册模块
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
        # 此处图像无预测框等信息
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
        os.system("python train_model.py")


        # 信息管理
    def manage_delete(self):
        mycursor = config.mydb.cursor()
        id = self.manage_input_id.text()
        mycursor.execute("delete from student where id = '%s'" % id)
        # 提交语句
        config.mydb.commit()
        self.manage_input_id.clear()
        self.manage_input_name.clear()
        self.manage_input_passwd.clear()
    def manage_change(self):
        mycursor = config.mydb.cursor()
        mycursor.execute("update student set name=%s,work=%s ,tel=%s where id=%s",
                         [self.manage_input_name_2.text(), self.manage_input_work.text(), self.manage_input_tel.text(),self.manage_input_id_2.text()])
        config.mydb.commit()
        self.manage_input_id_2.clear()
        self.manage_input_name_2.clear()
        self.manage_input_tel.clear()
        self.manage_input_work.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = myMainWindow()
    ui.show()
    sys.exit(app.exec_())
