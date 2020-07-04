#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ldap3
import re

def get_plugin_info():
    plugin_info = {
        "name": "ldap 未授权",
        "desc": "导致数据库敏感信息泄露，严重可导致服务器被入侵。",
        "grade": "高",
        "type": "service",
        "keyword": "service:ldap port:389",
    }
    return plugin_info

def poc(arg):
    check_port = lambda x:x if re.match(r"(.*?):(\d+)$",x) else x+':389'
    host,port = check_port(arg).split(':')
    timeout = 5
    try:
        server = ldap3.Server(host, get_info=ldap3.ALL, connect_timeout=timeout)
        conn = ldap3.Connection(server, auto_bind=True)
        if len(server.info.naming_contexts) > 0:
            return True
    except Exception:
        return


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("{} IP[:port]".format(sys.argv[0]))
    else:
        print("{} {}".format(sys.argv[1],poc(sys.argv[1])))  
