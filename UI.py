#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Py40 PyQt5 tutorial

This program creates a skeleton of
a classic GUI application with a menubar,
toolbar, statusbar, and a central widget.

author: Jan Bodnar
website: py40.com
last edited: January 2015
"""

import sys
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from Capture import *
import os
from PyQt5.QtCore import QStringListModel
from multiprocessing import Process

# name_device = ""
# CapturePid = 0
#
# def change():
#     capture(name_device)


class Example(QMainWindow):

    nameofDevice = ""
    captureFlag = False
    list = []
    # thread = myThread(1,"caption")


    def __init__(self):
        super().__init__()

        self.initUI()

    def initNetList(self):
        list = showDevice()
        for i in range(len(list)):
            self.combo.addItem(list[i])


    def deviceOnChoose(self,text):
        self.nameofDevice = text


    def beginCapture(self):
        if self.captureFlag == False:
            self.captureFlag = True
            thread = myThread(1,"caption",self.nameofDevice)
            self.list.append(thread)
            beginCapture(thread)

    def endCapture(self):
        self.captureFlag = False
        endCapture(self.list[0])

    def get_item_store(self,arg1):
        weidge = QWidget()
        hbox = QHBoxLayout()

        time = QLabel()
        time.setText(arg1[0])
        hbox.addWidget(time)

        source = QLabel()
        source.setText(arg1[1])
        hbox.addWidget(source)

        Destination = QLabel()
        Destination.setText(arg1[2])
        hbox.addWidget(Destination)

        protocol = QLabel()
        protocol.setText(arg1[3])
        hbox.addWidget(protocol)

        Info = QLabel()
        Info.setText(arg1[4])
        hbox.addWidget(Info)

        weidge.setLayout(hbox)
        return weidge

    def dataLoad(self):
        for i in range(20):
            item = QListWidgetItem()  # 创建QListWidgetItem对象
            item.setSizeHint(QSize(20, 45))  # 设置QListWidgetItem大小
            widget = self.get_item_store(["64 0.8374638", "124.12.3.1", "22.3.1.4", "IPv6", "Info"])  # 调用上面的函数获取对应
            self.listView.addItem(item)  # 添加item
            self.listView.setItemWidget(item, widget)  # 为item设置widget



    def clickedlist(self, item):
        #QMessageBox.information(self, "QListView", "你选择了: " + self.qList[qModelIndex.row()])
        print("点击的是：" + str(item.row()))

    def initUI(self):

        self.setGeometry(300,100,1350,900)#窗体大小
        self.setWindowTitle('MySniff')#标题
        self.setWindowIcon(QIcon('icon/spotify.png'))#图标

        title = QLabel('Packet List')
        author = QLabel('Packet Details')
        review = QLabel('Packet in Binary')

        #self.ListView = QListView()
        DetailsView = QTextEdit()
        BinaryView = QTextEdit()

        grid = QGridLayout()
        grid.setSpacing(10)

        self.listView = QtWidgets.QListWidget()  # 创建一个listview对象
        self.dataLoad()
        self.listView.clicked.connect(self.clickedlist)  # listview 的点击事件

        grid.addWidget(title, 1, 0)
        grid.addWidget(self.listView, 1, 1)

        grid.addWidget(author, 2, 0)
        grid.addWidget(DetailsView, 2, 1)

        grid.addWidget(review, 3, 0)
        grid.addWidget(BinaryView, 3, 1, 5, 1)

        mainWidget = QWidget()
        mainWidget.setLayout(grid)

        self.setCentralWidget(mainWidget)

        runAction = QAction(QIcon('icon/run.png'), 'run', self)
        runAction.setShortcut('Ctrl+r')
        runAction.setStatusTip('run capture')
        runAction.triggered.connect(self.beginCapture)

        stopAction = QAction(QIcon('icon/stop.png'), 'stop', self)
        stopAction.setShortcut('Ctrl+s')
        stopAction.setStatusTip('stop capture')
        stopAction.triggered.connect(self.endCapture)

        self.statusBar()

        toolbar = self.addToolBar('run')
        toolbar.addAction(runAction)

        toolbar = self.addToolBar('stop')
        toolbar.addAction(stopAction)

        self.combo = QComboBox(self)
        toolbar.addWidget(self.combo)
        self.combo.activated[str].connect(self.deviceOnChoose)

        self.initNetList()
        self.show()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    print("主进程",os.getpid())
    ex = Example()
    sys.exit(app.exec_())