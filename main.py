import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from register import Ui_MainWindow
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
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.save_information)
        self.pushButton.clicked.connect(self.paintEvent)
        self.retinaface = Retinaface()
        openni2.initialize()
        self.dev = openni2.Device.open_any()
        self.color_stream = self.dev.create_color_stream()
        self.color_stream.start()
        self.painter = QPainter(self)


   # 保存相应数据到数据库
    def save_information(self):

        mycursor = config.mydb.cursor()
        sql = "INSERT INTO student (id, name, telephone, password, class) VALUES (%s, %s, %s, %s, %s)"
        val = (self.id.text(), self.name.text(), self.name.text(), self.tellphone.text(), self.classes.text())
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
        cframe_data = np.transpose(np.array([B, G, R]), [1, 2, 0])
        cframe_data = np.array(self.retinaface.detect_image(cframe_data))
        fps = (fps + (1. / (time.time() - t1))) / 2
        cframe_data= cv2.putText(cframe_data, "fps= %.2f" % (fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                                   2)

        self.Qframe = QImage(cframe_data.data.tobytes(), cframe_data.shape[1], cframe_data.shape[0], cframe_data.shape[1] * 3,
                             QImage.Format_RGB888)
        self.video.setPixmap(QPixmap.fromImage(self.Qframe))
        self.update()
        c = cv2.waitKey(1) & 0xff
        if c == ord('s'):
            i += 1
            name = id
            cv2.imencode('.jpg', cframe_data)[1].tofile('face_dataset/' + name + '_' + str(i) + '.jpg')
            print(i)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = myMainWindow()
    ui.show()
    sys.exit(app.exec_())
