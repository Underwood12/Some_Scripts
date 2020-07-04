#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from dns import resolver

def poc(arg):
    ip_list = []
    try:
        arg = arg.strip()
        ans = resolver.query(arg, "A")
        for i in ans.response.answer:
            for ip in i.items:
                if ip.rdtype == 1:
                    ip_list.append(ip.address)

    except Exception as e:
        return
    return "{}\t{}".format(arg,",".join(ip_list))

if __name__ == "__main__":
    print(poc("baidu.com"))
