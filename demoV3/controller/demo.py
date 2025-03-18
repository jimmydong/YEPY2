# -*- coding: utf-8 -*-
"""
这是一个子模块的Demo
每一个Blueprint相当于一个controller
开发指导：
  1，修改或添加route规则（如果需要的话）
  2，开发处理逻辑（建议按照“add your code here”）
  3，修改config.py，将controller名字加入到blueprints列表中
"""
from flask import Blueprint, render_template, abort, request, current_app, make_response
from . import *
import bucketV3 as bucket
import config
import os
### 以上为必备的模块，应用所需模块请在此下继续添加 ###
import time

controller = os.path.basename(__file__).split('.',1)[0]
blueprint = Blueprint(controller, __name__, url_prefix='/%s' % controller)

#action
@blueprint.route('/', defaults={'action':'index'}, methods=['GET','POST'])
@blueprint.route('/<action>', methods=['GET','POST'])
@blueprint.route('/<action>/', methods=['GET','POST'])
def main(action):
    ############################################################################
    # init
    ############################################################################
    bucket._controller = controller
    bucket._action = action
    out = init()
    out['title'] = 'HELP'
    out['headline'] = '操作指南（待补充）'
    
    ############################################################################
    # add your code here
    ############################################################################
    out['time'] = time.strftime("%Y-%m-%d %H:%M:%S")
    bucket.debug.time("action " + action + " begin")
    
    #处理action
    if action == 'index':
        do = request.args.get('do')
        log = current_app.logger.debug
        log(do)
        print(do)
        if do == '1':
            #测试全局类
            g = bucket.G
            if not g.get('jobCounter'):
                g.jobCounter = 1
            else:
                g.jobCounter += 1
            out.data = g.jobCounter
        elif do == '2':
            #测试缓存
            key = 'demoV3_test'
            if not bucket.cache.get(key):
                bucket.cache.set(key,'---kakaka, cache works OK!---')
            else:
                bucket.cache.set(key, bucket.cache.get(key) + '.')
            out.data = "Cache: %s" % bucket.cache.get(key)
        else:
            out.data = "展开 firebug 查看 debug 信息 ， 点击右侧FDT查看 logger 信息"
            out.data = out.data + "<br/>\n 工作线程信息： %s" % bucket.G.jobCounter
            #使用logger(记录到app.log文件)
            current_app.logger.debug('test logger')
            current_app.logger.warning('warning')
            #使用Debug(FirePhp或debugtools显示)
            bucket.debug.time("action " + action + " end")
            bucket.debug.log('debug:out', out)

    elif action == 'help':
        bucket.debug.log('test', 'hello')
        bucket.debug.show()
        out['alert'] = request.args.get('alert')
        
    else: 
        #do something
        error = "未定义的action" 
    

    ############################################################################
    # finish
    ############################################################################
    return show(out)
