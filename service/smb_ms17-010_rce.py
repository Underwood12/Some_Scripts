#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
import socket

def get_plugin_info():
    plugin_info = {
        "name": "MS17-010远程溢出漏洞（CVE-2017-0143）",
        "desc": "存在MS17-010远程溢出漏洞",
        "grade": "高",
        "type": "service",
        "keyword": "service:microsoft-ds cve:CVE-2017-0143 tag:ms17-010 tag:smb port:445"
    }
    return plugin_info

def poc(arg):
    check_port = lambda x:x if re.match(r"(.*?):(\d+)$",x) else x+':445'
    host,port = check_port(arg).split(':')
    timeout = 5
    negotiate_protocol_request = bytes.fromhex("00000054ff534d42720000000018012800000000000000000000000000002f4b0000c55e003100024c414e4d414e312e3000024c4d312e325830303200024e54204c414e4d414e20312e3000024e54204c4d20302e313200")
    session_setup_request = bytes.fromhex("00000063ff534d42730000000018012000000000000000000000000000002f4b0000c55e0dff000000dfff02000100000000000000000000000000400000002600002e0057696e646f7773203230303020323139350057696e646f7773203230303020352e3000")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, int(port)))
        s.send(negotiate_protocol_request)
        s.recv(1024)
        s.send(session_setup_request)
        data = s.recv(1024)
        user_id = data[32:34]
        tree_connect_andx_request = "000000%xff534d42750000000018012000000000000000000000000000002f4b%sc55e04ff000000000001001a00005c5c%s5c49504324003f3f3f3f3f00" % ((58 + len(host)), user_id.hex(), host.encode().hex())
        s.send(bytes.fromhex(tree_connect_andx_request))
        data = s.recv(1024)
        allid = data[28:36]
        payload = "0000004aff534d422500000000180128000000000000000000000000%s1000000000ffffffff0000000000000000000000004a0000004a0002002300000007005c504950455c00" % allid.hex()
        s.send(bytes.fromhex(payload))
        data = s.recv(1024)
        s.close()
        if b"\x05\x02\x00\xc0" in data:
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

