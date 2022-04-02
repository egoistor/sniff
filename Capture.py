import os

from winpcapy import WinPcapDevices, WinPcap
from winpcapy import WinPcapUtils
from dpkt.utils import mac_to_str, inet_to_str
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

    t = threading.current_thread()
    #print('Ethernet Frame: ', mac_to_str(eth.src), mac_to_str(eth.dst), eth.type)

    #eth.pprint()


class myThread (threading.Thread):
    def __init__(self, threadID, name, name_device = ""):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.name_device = name_device
        self.pcap = WinPcap(name_device)

    def run(self):
        file = open("test.txt", 'w').close()
        print(self.name_device)
        device_name, desc = WinPcapDevices.get_matching_device(self.name_device)
        if device_name is not None:
            with WinPcap(device_name) as winpcap:
                self.pcap = winpcap
                winpcap.run(callback=packet_callback)

    def stop(self):
        try:
            self.pcap.stop()
        except:
            print("出现了问题")


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
