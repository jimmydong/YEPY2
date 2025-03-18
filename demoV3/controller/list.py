# -*- coding: utf-8 -*-
"""
列表模块
"""
from flask import Blueprint, render_template, abort, request, current_app, make_response
from . import *
import bucketV3 as bucket
import config
import os
### 以上为必备的模块，应用所需模块请在此下继续添加 ###
import time
import func_pack
import sqlite_db
import xml_to_redis

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
    out['title'] = 'List'
    out['headline'] = '历史上传查看'
    
    ############################################################################
    # add your code here
    ############################################################################
    
    #验证cookie
    user_name, user_id = func_pack.decode_user_cookie(request.cookies.get('HAMSTER'))
    if user_name == None:
        return redirect('/', '未登录或权限不正确', '未登录或权限不正确，请重新登录')
    #处理action
    if action == 'index':
        rows = sqlite_db.list_upload()
        out['rows'] = rows
    elif action == 'redis': #查看redis
        redis_key = request.args['redis_key']
        data = xml_to_redis.redis_get(redis_key)
        if data is None:
            out['alert'] = '读取数据失败'
        else:
            out['info'] = redis_key
            out['data'] = str(data, encoding='utf-8')
    elif action == 'download': #下载
        upload = sqlite_db.get_upload(request.args['id'])
        if upload == None:
            return error("/list/", "下载错误")
        
        response = make_response(upload['xml_data'])
        response.headers["Content-Disposition"] = f"attachment; filename={upload['xml_filename']}"
        return response
    else: 
        #do something
        return redirect('/', '404:页面未找到')
    

    ############################################################################
    # finish
    ############################################################################
    return show(out)
