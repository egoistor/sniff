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
                ip_flag = False
                llc_flag = False
                l = []
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
                        if "dst=" in file_path:
                            try:
                                strlist = file_path.split('#')
                                dst = strlist[1]
                            except:
                                pass
                            # print(dst)

                        if "src=" in file_path:
                            try:
                                strlist = file_path.split('#')
                                src = strlist[1]
                            except:
                                pass

                            # print(src)

                        if "data=ARP" in file_path:
                            protocol = "ARP"

                        if "data=LLC" in file_path:
                            protocol = "LLC"
                            llc_flag = True

                        if llc_flag:
                            if "data=STP" in file_path:
                                protocol = protocol + "-STP"

                        if "v=4" in file_path:
                            protocol = "IPv4"
                            ip_flag = True

                        if "v=6" in file_path:
                            protocol = "IPv6"
                            ip_flag = True

                        if ip_flag:
                            if "src=" in file_path:
                                try:
                                    strlist = file_path.split('#')
                                    src = strlist[1]
                                except:
                                    pass
                            if "dst=" in file_path:
                                try:
                                    strlist = file_path.split('#')
                                    dst = strlist[1]
                                except:
                                    pass
                            if "data=UDP" in file_path:
                                protocol = protocol + "-UDP"
                            if "data=TCP" in file_path:
                                protocol = protocol + "-TCP"
                            if "data=ICMP6" in file_path:
                                protocol = protocol + "-ICMP6"
                            if "data=IGMP" in file_path:
                                protocol = protocol + "-IGMP"

                    if file_path == ")  # Ethernet":
                        l.append(str(file_path))
                        begin_flag = False
                        ip_flag = False
                        llc_flag = False
                        show_list = [dst, src, protocol]
                        data_l = [show_list, l]
                        self.update_date.emit(data_l)
                        l.clear()
                        time.sleep(0.05)
            else:
                pass


if __name__ == '__main__':
    print()