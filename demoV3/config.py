# -*- coding: utf-8 -*-
""" 
YEPY 核心配置文件
"""
import sys
import os
import re
import codecs

with codecs.open('__init__.py', encoding='utf-8') as fp:
    content = fp.read()
    app_version = re.search(r"__version__\s*=\s*'([\w\-.]+)'", content).group(1)
    app_name = re.search(r"__title__\s*=\s*'([\w\-.]+)'", content).group(1)

_yepy_application_version = '1.3b'
_yepy_path = '../'
sys.path.append(_yepy_path) #如果yepy不在当前目录

is_debug = False
if len(sys.argv) > 1:
    if sys.argv[1] == 'debug':
        is_debug = True
is_firedebug = False

#Flask配置
class Config(object):
    APP_NAME = app_name
    APP_HOST = '0.0.0.0'
    APP_PORT = 8099
    DEBUG = False
    USE_RELOADER = False                # 禁止代码自动更新，防止运行多次
    TESTING = False
    SECRET_KEY = "01234567890@2015"
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SESSION_COOKIE_NAME = "YEPY_SESSION"
    
    CACHE_ENABLE = True
    CACHE_KEY_PREFIX = "YEPY_" 
    CACHE_MEMCACHED_SERVERS = ["127.0.0.1:11211"]
    
    UPLOADS_DEFAULT_DEST = "static/upload"
    UPLOADS_DEFAULT_URL = "/upload"
    #UPLOADED_FILES_ALLOW = []
    #UPLOADED_FILES_DENY = []
    
    LOG_FILE = 'app.log'
    LOG_SIZE = 10000
    
class DevelopmentConfig(Config):
    DEBUG = True
    DEBUG_TB_PROFILER_ENABLED = True  #注意：极大影响性能
    
class ProductionConfig(Config):
    DEBUG = False
    DEBUG_TB_PROFILER_ENABLED = False
    
    
# 应用模块
blueprints = [
              'controller.default:blueprint',
              'controller.demo:blueprint'
              ]
