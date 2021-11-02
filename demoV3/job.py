# -*- coding: utf-8 -*-
""" 
DEMO: 完成工作任务的子线程
by jimmy.dong@gmail.com 2015.01.14
"""
import bucketV3 as bucket # 加载全局变量
import config
import time

def myJob():
    # Do something
    while True:
        if not bucket.G.get('jobCounter'):
            bucket.G.jobCounter = 1
        else:
            bucket.G.jobCounter += 1
        
        if config.is_debug:
            print('job running ...' + str(bucket.G.jobCounter))
        else:
            with open('heartbit.log', 'w') as f:
                f.write(time.strftime("%Y-%m-%d %H:%M:%S"))            
        time.sleep(3)
    pass