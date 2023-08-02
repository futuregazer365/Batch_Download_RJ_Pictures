from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
from Ui_untitled import Ui_MainWindow
from dialog import MyDialog, MySignal
import sys, math
import requests
import re
import os
from bs4 import BeautifulSoup

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)  # 初始化父类
        self.setupUi(self)  # 继承 Ui_MainWindow 界面类
        self.pushButton.clicked.connect(self.onbtnImport)
        self.pushButton_2.clicked.connect(self.onbtndownload)
        self.storagePath = ""
        self.rjlist = ""
        self.url = "https://www.dlsite.com/maniax/work/=/product_id/RJ01052122.html"
        self.directory = 'downloaded_RJimages'

    def onbtnImport(self):
        """
        导入RJ号槽函数
        """
        self.dialog = MyDialog(self)
        self.dialog.my_signal.my_signal.connect(self.onReceive)
        self.dialog.exec()

    def onReceive(self,strdata):
        """
        self.dialog实例化后链接的槽函数
        用于接受自定义信号发送的数据
        """
        # 将RJtext分割为RJ数组
        self.rjlist = self.split_string_by_newline(strdata)
        # 清空列表中的项
        self.listWidget.clear()
        # 获取所有项并为每个项开启编辑
        # 创建并显示字符串项
        for rj_string in self.rjlist:
            if rj_string:
                item = QListWidgetItem(rj_string)
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                self.listWidget.addItem(item)

    def split_string_by_newline(self,input_string):
        """
        接受RJ字串，将其分割为RJ编号列表
        """
        string_array = input_string.split("\n")
        return string_array

    def onbtndownload(self):
        # 创建目录存储下载的图片
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        # 获取listWidget的item
        for row in range(self.listWidget.count()):
            item = self.listWidget.item(row)
            # 获取一条RJ信息
            item_text = item.text()
            if item_text:
                # 组建访问URL，图片文件名
                rj_number = re.sub(r"(?i)RJ", "", item_text)  # 删除 "RJ" 前缀，不区分大小写
                accessedurl = re.sub(r"01052122", rj_number, self.url, flags=re.IGNORECASE)  # 替换 RJ 号，不区分大小写
                filename = item_text + ".jpg"
                # 发起 GET 请求获取网页内容
                response = requests.get(accessedurl)
                html = response.text
                # 使用BeautifulSoup解析网页内容
                soup = BeautifulSoup(html, 'html.parser')
                img_url = soup.find("meta", attrs={"property": "og:image"})["content"]
                print(img_url)
                response = requests.get(img_url)
                if response.status_code == 200:
                    filepath = os.path.join(self.directory, filename)
                    with open(filepath, "wb") as f:
                        f.write(response.content)
                    print("图片下载完成")
                else:
                    print("图片下载失败")







if __name__ == '__main__':  # youcans, XUPT 2021

    app = QApplication(sys.argv)  # 在 QApplication 方法中使用，创建应用程序对象
    myWin = MyMainWindow()  # 实例化 MyMainWindow 类，创建主窗口
    myWin.show()  # 在桌面显示控件 myWin
    sys.exit(app.exec_())  # 结束进程，退出程序