import sys
from PyQt5.QtCore import QSize, QThread, pyqtSignal, QDateTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from Capture import *
import os
from PyQt5.QtCore import QStringListModel
from multiprocessing import Process

from sniff.UtilThread import BackendThread


class Example(QMainWindow):
    nameOfDevice = ""
    captureFlag = False
    reFlashFlag = False
    list = []
    deviceList = []
    cap_info_list = []

    threadID = 0
    thread = BackendThread()

    # thread = myThread(1,"caption")

    def __init__(self):
        super().__init__()

        self.initUI()
        self.initFlashUI()

    def initNetList(self):
        deviceList = showDevice()
        for i in range(len(deviceList)):
            self.combo.addItem(deviceList[i])

    def initFlashUI(self):
        # 注册信号处理函数
        self.thread.update_date.connect(self.dataLoad)
        # 启动线程
        self.thread.start()

    def deviceOnChoose(self, text):
        self.nameOfDevice = text

    def beginCapture(self):
        if len(self.nameOfDevice) == 0:
            QMessageBox.information(self, "warning", "请先选择设备")
        else:
            if not self.captureFlag:
                if not self.reFlashFlag:
                    self.captureFlag = True
                    self.thread.lock = True
                    print(self.nameOfDevice)
                    thread = myThread(1, "caption", self.nameOfDevice)
                    self.list.append(thread)
                    beginCapture(thread)
                else:
                    QMessageBox.information(self, "warning", "无法更新UI")
            else:
                QMessageBox.information(self, "warning", "请先停止抓包")

    def endCapture(self):
        if self.captureFlag:
            self.captureFlag = False
            self.thread.lock = False
            endCapture(self.list[self.threadID])
            self.threadID = self.threadID + 1
        else:
            QMessageBox.information(self, "warning", "请先开始抓包")

    def getItemStore(self, arg1):
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

        weidge.setLayout(hbox)
        return weidge

    def dataLoad(self, data):
        str = ""
        for i in range(len(data)):
            str = str + data[i] + "\n"
        self.DetailsView.setText(str)

    def clickedlist(self, item):
        # QMessageBox.information(self, "QListView", "你选择了: " + self.qList[qModelIndex.row()])
        print("点击的是：" + str(item.row()))

        self.DetailsView.setText(self.capList[item.row() * 2])
        self.BinaryView.setText(str(self.capList[item.row() * 2 + 1]))

    def initUI(self):

        self.setGeometry(300, 100, 1350, 900)  # 窗体大小
        self.setWindowTitle('MySniff')  # 标题
        self.setWindowIcon(QIcon('icon/spotify.png'))  # 图标

        title = QLabel('Packet List')
        author = QLabel('Packet Details')
        review = QLabel('Packet in Binary')

        # self.ListView = QListView()
        self.DetailsView = QTextEdit()

        grid = QGridLayout()
        grid.setSpacing(10)

        self.listView = QtWidgets.QListWidget()  # 创建一个listview对象
        self.listView.clicked.connect(self.clickedlist)  # listview 的点击事件

        grid.addWidget(title, 1, 0)
        grid.addWidget(self.listView, 1, 1)

        grid.addWidget(author, 2, 0)
        grid.addWidget(self.DetailsView, 2, 1)

        # grid.addWidget(review, 3, 0)
        # grid.addWidget(self.BinaryView, 3, 1, 5, 1)

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
    print("主进程", os.getpid())
    ex = Example()
    sys.exit(app.exec_())
