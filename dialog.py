from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidget, QListWidgetItem, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QObject, pyqtSignal
import sys
from Ui_dialog import Ui_Dialog

# 创建自定义的信号类
class MySignal(QObject):
    # 定义自定义信号
    my_signal = pyqtSignal(str)  # 信号参数可以根据需要进行定义

class MyDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)  # 初始化父类
        self.setupUi(self)  # 继承 Ui_MainWindow 界面类
        self.pushButton.clicked.connect(self.onbtnConfirm)
        self.rjtext = " "
        self.sender = QObject()  # 将 sender 设置为类成员变量
        self.my_signal = MySignal()  # 将 my_signal 设置为类成员变量

    def onbtnConfirm(self):
        self.rjtext = self.textEdit.toPlainText()
        print(self.rjtext)
        # 发送自定义信号
        self.my_signal.my_signal.emit(self.rjtext)