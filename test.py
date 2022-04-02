import re

def text_del():
    srcFiles = open('test.txt', 'r')
    begin_flag = False
    ip_flag = False
    llc_flag = False
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

            if "dst=" in file_path:
                strlist = file_path.split('#')
                dst = strlist[1]
                #print(dst)

            if "src=" in file_path:
                strlist = file_path.split('#')
                src = strlist[1]
                #print(src)

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
                    strlist = file_path.split('#')
                    src = strlist[1]
                if "dst=" in file_path:
                    strlist = file_path.split('#')
                    dst = strlist[1]
                if "data=UDP" in file_path:
                    protocol = protocol + "-UDP"
                if "data=TCP" in file_path:
                    protocol = protocol + "-TCP"
                if "data=ICMP6" in file_path:
                    protocol = protocol + "-ICMP6"

        if file_path == ")  # Ethernet":
            l.append(str(file_path))
            begin_flag = False
            ip_flag = False
            llc_flag = False
            break

    for i in range(len(l)):
        print(l[i])
    print("dst is ", dst)
    print("src is ", src)
    print("protocol is", protocol)


if __name__ == '__main__':
    text_del()


    # line = "this hdr-biz 123 model server 456"
    # pattern = "model"
    # if pattern in line:
    #     print("matchObj")
