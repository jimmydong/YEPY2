# -*- coding: utf-8 -*-
'''
项目配置文件

'''
import sys
import os

_yepy_application_version = '1.3b'
_yepy_path = '../'
sys.path.append(_yepy_path) #如果yepy不在当前目录

root_path = os.path.split(os.path.realpath(__file__))[0]
http_port = 8099
run_percecond = 5
