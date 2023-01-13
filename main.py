# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QApplication

# 添加的所需库文件
from PyQt5 import QtCore, QtGui, QtWidgets
# mainwindow.ui Python文件
import mainwindow

if __name__ == "__main__":
    app = QApplication([])

    # 此处调用GUI的程序
    widgets = QtWidgets.QMainWindow()
    ui = mainwindow.Ui_MainWindow()
    ui.setupUi(widgets)
    widgets.show()
    # 结束

    sys.exit(app.exec_())