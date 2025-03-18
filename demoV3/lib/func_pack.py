# -*- coding: utf-8 -*-
'''
常用函数集成封装
'''
import hashlib

def md5_encode(string):
    try:
        md5 = hashlib.md5()
        md5.update(string.encode('utf-8'))
        return md5.hexdigest()
    except:
        return None


#编码用户cookie
def encode_user_cookie(name, id):
    t = md5_encode(name + str(id))
    code = name + '|' + t[6:16] + '|' + str(id)
    return code

#解码用户cookie
def decode_user_cookie(hamster):
    if type(hamster) is not str:
        return None, None
    t = hamster.split('|')
    if len(t) < 3:
        return None, None
    code = md5_encode(t[0] + t[2])
    if not code or t[1] != code[6:16]:
        return None, None
    else:
        return t[0], int(t[2])