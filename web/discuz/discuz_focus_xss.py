#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import hashlib
import requests
from urllib.parse import urlparse

requests.packages.urllib3.disable_warnings()

def get_plugin_info():
    plugin_info = {
        "name": "Disucz! x3.0 focus.swf XSS",
        "desc": "Discuz! x3.0 /static/image/util/focus.swf 存在Flash XSS漏洞",
        "grade": "中",
        "type": "web",
        "keyword": "tag:Discuz!7.x"
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
            url=f'{urlparse(arg).scheme}://{urlparse(arg).netloc}/static/image/util/focus.swf', 
            headers=headers,
            timeout=timeout, 
            verify=False
            )
        if r.status_code == 200 and hashlib.md5(r.content).hexdigest() == "c16a7c6143f098472e52dd13de85527f":
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

