# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1343, 855)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setMaximumSize(QtCore.QSize(500, 16777215))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout.setContentsMargins(30, -1, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.tellphone = QtWidgets.QLineEdit(self.frame_2)
        self.tellphone.setObjectName("tellphone")
        self.gridLayout.addWidget(self.tellphone, 2, 3, 1, 1)
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 1, 1, 1)
        self.password = QtWidgets.QLineEdit(self.frame_2)
        self.password.setObjectName("password")
        self.gridLayout.addWidget(self.password, 3, 3, 1, 1)
        self.classes = QtWidgets.QLineEdit(self.frame_2)
        self.classes.setObjectName("classes")
        self.gridLayout.addWidget(self.classes, 4, 3, 1, 1)
        self.id = QtWidgets.QLineEdit(self.frame_2)
        self.id.setObjectName("id")
        self.gridLayout.addWidget(self.id, 0, 3, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame_2)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 4, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 4, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frame_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 1, 1, 1)
        self.name = QtWidgets.QLineEdit(self.frame_2)
        self.name.setObjectName("name")
        self.gridLayout.addWidget(self.name, 1, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 4, 4, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.frame_2)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 5, 3, 1, 1)
        self.horizontalLayout.addWidget(self.frame_2)
        self.widget = QVideoWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.video = QtWidgets.QLabel(self.widget)
        self.video.setGeometry(QtCore.QRect(130, 130, 581, 480))
        self.video.setMaximumSize(QtCore.QSize(640, 480))
        self.video.setObjectName("video")
        self.horizontalLayout.addWidget(self.widget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1343, 28))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "密码"))
        self.label_5.setText(_translate("MainWindow", "班级"))
        self.label_4.setText(_translate("MainWindow", "学号"))
        self.label_3.setText(_translate("MainWindow", "姓名"))
        self.label_2.setText(_translate("MainWindow", "联系方式"))
        self.pushButton.setText(_translate("MainWindow", "确定"))
        self.video.setText(_translate("MainWindow", "TextLabel"))
from PyQt5.QtMultimediaWidgets import QVideoWidget
