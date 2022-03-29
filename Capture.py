import os

from winpcapy import WinPcapDevices, WinPcap
from winpcapy import WinPcapUtils

import dpkt
import time
import datetime
import threading

# print(list_device)

def showDevice():
    list = []
    for device in WinPcapDevices.list_devices():
        list.append(WinPcapDevices.list_devices()[device])
    return list


def packet_callback(win_pcap, param, header, pkt_data):
    eth = dpkt.ethernet.Ethernet(pkt_data)
    # 判断是否为IP数据报
    # if not isinstance(eth.data, dpkt.ip.IP):
    #     print("Non IP packet type not supported ", eth.data.__class__.__name__)
    #     return
    #抓IP数据包
    # print()
    # packet = eth.data
    # print(eth.data.__class__.__name__)
    # print(packet)

    t = threading.current_thread()
    print("capture thread:",t)

    # 取出分片信息
    # df = bool(packet.off & dpkt.ip.IP_DF)
    # mf = bool(packet.off & dpkt.ip.IP_MF)
    # offset = packet.off & dpkt.ip.IP_OFFMASK

    #输出数据包信息：time,src,dst,protocol,length,ttl,df,mf,offset,checksum
    # output1 = {'time':time.strftime('%Y-%m-%d %H:%M:%S',(time.localtime()))}
    # output2 = {'src':'%d.%d.%d.%d'%tuple(packet.src) , 'dst':'%d.%d.%d.%d'%tuple(packet.dst)}
    # output3 = {'protocol':packet.p, 'len':packet.len, 'ttl':packet.ttl}
    #output4 = {'df':df, 'mf':mf, 'offset':offset, 'checksum':packet.sum}

    # print(output1)
    # print(output2)
    # print(output3)
    #print(output4)



    #WinPcapUtils.capture_on(pattern=name_device, callback=packet_callback)


class myThread (threading.Thread):
    def __init__(self, threadID, name, name_device = ""):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.name_device = name_device
        self.pcap = WinPcap(name_device)

    def run(self):
        print(self.name_device)
        device_name, desc = WinPcapDevices.get_matching_device(self.name_device)
        if device_name is not None:
            with WinPcap(device_name) as winpcap:
                self.pcap = winpcap
                winpcap.run(callback=packet_callback)

    def stop(self):
        # try:
        self.pcap.stop()
        # except:
        #     print("出现了问题")


def beginCapture(thread):
    thread.start()


def endCapture(thread):
    print("end thread:",thread)
    thread.stop()



if __name__ == '__main__':
    deviceList = showDevice()
    for i in range(len(deviceList)):
        print(deviceList[i])
    capture(deviceList[5])

