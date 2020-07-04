#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
from urllib.parse import urlparse

requests.packages.urllib3.disable_warnings()

def get_plugin_info():
    plugin_info = {
        "name": "ElasticSearch 未授权访问",
        "desc": "未授权访问导致数据信息泄露，部分版本或插件存在漏洞，严重可导致服务器被入侵。",
        "grade": "中",
        "type": "web",
        "keyword": "tag:elasticSearch port:9200"
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
            url=f'{urlparse(arg).scheme}://{urlparse(arg).netloc}/_cat', 
            headers=headers,
            timeout=timeout, 
            verify=False
            )
        if r.status_code == 200 and "/_cat/master" in r.text:
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

