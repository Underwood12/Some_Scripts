#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import random
import requests
from urllib.parse import urlparse

requests.packages.urllib3.disable_warnings()

def get_plugin_info():
    plugin_info = {
        "name": "目录可列",
        "desc": "攻击者通过此漏洞查看文件",
        "grade": "中",
        "type": "web",
        "keyword": "tag:web",
    }
    return plugin_info

def poc(arg):
    arg = arg if "://" in arg else f"http://{arg}"
    timeout = 5
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
        'Referer': arg
        }
    flag_list = [
        "<title>index of",
        "<title>directory listing for",
        f"<title>{urlparse(arg).netloc} - /"
    ]
    url_list = [f'{urlparse(arg).scheme}://{urlparse(arg).netloc}/{i}/' for i in ["css","js","images","upload","inc"]]
    error_i=0
    for url in url_list:
        try:
            r = requests.get(
                url=f'{urlparse(arg).scheme}://{urlparse(arg).netloc}', 
                headers=headers,
                timeout=timeout, 
                verify=False
                )

        except requests.exceptions.ConnectionError:
            return
        except requests.HTTPError:
            return
        except:
            error_i += 1
            if error_i >= 3:
                return
            continue
        if r.status_code == 404:
            continue
        for flag in flag_list:
            if flag in r.text:
                return url
                
if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("{} URL".format(sys.argv[0]))
    else:
        print("{} {}".format(sys.argv[1],poc(sys.argv[1])))  

