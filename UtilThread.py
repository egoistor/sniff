import threading

from PyQt5.QtCore import QThread ,  pyqtSignal,  QDateTime
from PyQt5.QtWidgets import QApplication,  QDialog,  QLineEdit
import time
import sys

class BackendThread(QThread):
    # 通过类成员对象定义信号
    update_date = pyqtSignal(list)
    lock = False
    # 处理业务逻辑
    def run(self):
        while True:
            if self.lock:
                srcFiles = open('test.txt', 'r')
                begin_flag = False
                l = []
                show_list = []
                dst = ""
                src = ""
                protocol = ""
                for file_path in srcFiles:
                    file_path = file_path.rstrip()
                    if file_path == "Ethernet(":
                        begin_flag = True
                        l.append(str(file_path))
                    if begin_flag:
                        l.append(str(file_path))
                        pattern = "dst="
                        #if pattern in file_path:
                    if file_path == ")  # Ethernet":
                        l.append(str(file_path))
                        begin_flag = False
                        break
                self.update_date.emit(l)
                time.sleep(1)
            else:
                pass


if __name__ == '__main__':
    print()