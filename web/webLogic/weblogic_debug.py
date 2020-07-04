#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
from urllib.parse import urlparse

requests.packages.urllib3.disable_warnings()

def get_plugin_info():
    plugin_info = {
        "name": "Weblogic 任意文件上传漏洞",
        "desc": "配置中启用 Web 服务测试页后，未授权的两个页面存在任意上传getshell漏洞，利用该漏洞可以上传任意jsp文件，进而获取服务器权限。",
        "grade": "中",
        "type": "web",
        "keyword": "tag:weblogic cve:CVE-2018-2894"
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
            url=f'{urlparse(arg).scheme}://{urlparse(arg).netloc}/ws_utc/config.do', 
            headers=headers,
            timeout=timeout, 
            verify=False
            )
        if r.status_code == 200 and "Work Home Dir" in r.text:
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

