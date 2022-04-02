import threading

from PyQt5.QtCore import QThread ,  pyqtSignal,  QDateTime
from PyQt5.QtWidgets import QApplication,  QDialog,  QLineEdit
import time
import sys

class BackendThread(QThread):
    # 通过类成员对象定义信号
    update_date = pyqtSignal(str)
    lock = False
    # 处理业务逻辑
    def run(self):
        while True:
            if self.lock:
                data = QDateTime.currentDateTime()
                currTime = data.toString("yyyy-MM-dd hh:mm:ss")
                self.update_date.emit(str(currTime))
                time.sleep(1)
            else:
                pass

    # def setLock(self,new_bool):
    #     self.lock = new_bool

if __name__ == '__main__':
    print()