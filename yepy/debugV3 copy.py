# -*- coding: utf-8 -*-
"""
YEPY 调试辅助模块
by jimmy.dong@gmail.com 2016.1.4

由FirePHP改写，符合FirePHP规则
"""
from yepy import firephp
import sys
import traceback
import time
from yepy.hack_flask_toolbar import MyRecordHandler
from flask_debugtoolbar.panels import logger
logger.handler = MyRecordHandler()

class Debug:
    __debug_level = 'info'   # 三个调试等级['none', 'stat', 'info']
    __open = False
    __firephp = False
    __log_file = False
    __log_db = False
    __autolog_file = False
    __autolog_db = False
    time_table = []
    time_begin = 0
    log_table = []
    
    def __init__(self):
        self.firephp = firephp.FirePhp()
        self.reload()
        
    def reload(self):
        self.time_table = []
        self.time_table.append(["Description","Time","Caller"])
        self.time_begin = time.process_time()
        self.log_table = []
        self.log_table.append(["Label","Results","Caller"])
        self.firephp.reload()
    
    def config(self, **attrs):
        for (key,value) in attrs.items():
            tmp = value
            code = "self.%s = tmp" % key
            exec(code)
    
    # 开启
    def start(self):
        self.__open = True
    
    # 关闭
    def stop(self):
        self.__open = False
    
    # 是否开启
    def opened(self):
        return self.__open
    
    def time(self, label='', caller=''):
        if not self.__open:
            return False
        if label == '':
            label == '临时调试'
        if caller == '':
            try:
                raise Exception
            except:
                f = sys.exc_info()[2].tb_frame.f_back
                caller = "%s %s:%s" % (f.f_code.co_filename, f.f_code.co_name, f.f_lineno)
        self.time_table.append([label,"%2.6f" % (time.process_time()-self.time_begin),caller])
    
    def log(self, label, result='', caller=''):
        if not self.__open:
            return False
        
        if result == '':
            result = label
            label = '临时调试'
        if caller == '':
            try:
                raise Exception
            except:
                f = sys.exc_info()[2].tb_frame.f_back
                caller = "%s %s:%s" % (f.f_code.co_filename, f.f_code.co_name, f.f_lineno)
        # firephp
        self.log_table.append([label, result, caller])
        # flask-debug-toolbar
        logger.handler.add_record(label, time.time(), result, f.f_code.co_filename+' '+f.f_code.co_name, f.f_lineno)
        
    
    def flog(self):
        pass

    def dlog(self):
        pass

    def cache(self):
        pass
    
    def db(self):
        pass
    
    def show(self):
        self.firephp.fb(self.time_table, title="This Page Spend Times %f" % (time.process_time()-self.time_begin), skip=2)
        self.firephp.fb(self.log_table, title='Custom Log Object', skip=1)
        return self.firephp.headers
    
    
    
