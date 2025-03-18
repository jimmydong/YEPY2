# -*- coding: utf-8 -*-
"""
上传模块
"""
from flask import Blueprint, render_template, abort, request, current_app, make_response
from . import *
import bucketV3 as bucket
import config
import os
### 以上为必备的模块，应用所需模块请在此下继续添加 ###
import time
import xml_to_redis
import xml.dom.minidom
import func_pack
import sqlite_db
from werkzeug.utils import secure_filename

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
    out['title'] = 'XML Upload'
    out['headline'] = 'XML上传到Redis'

    ############################################################################
    # add your code here
    ############################################################################

    #验证cookie
    user_name, user_id = func_pack.decode_user_cookie(request.cookies.get('HAMSTER'))
    if user_name == None:
        return redirect('/', '未登录或权限不正确', '未登录或权限不正确，请重新登录')
    #处理action
    if action == 'index':
        out.info = ''
    elif action == 'submit':
        upload_file = request.files['upload_file']
        if not upload_file:
            out.alert = '上传失败'
        else:
            file_name = secure_filename(upload_file.filename)
            xml_string = upload_file.stream.read().decode("utf-8")
            key, value = xml_to_redis.handle_xml(xml_string, request.form['bid'], request.form['table'])
            if key is None:
                out.alert = '解析失败，请检查参数和XML文件'
            else:
                ret = sqlite_db.insert_upload(user_id=user_id, business_id=request.form['bid'], structure=request.form['table'], 
                                        redis_key=key, redis_value=value, xml_filename=file_name, xml_data=xml_string)
                if ret is None:
                    out.alert = '写入数据库失败'
                else:
                    dom = xml.dom.minidom.parseString(value)
                    pretty_xml = dom.toprettyxml(indent="    ", encoding="utf-8").decode("utf-8")
                    pretty_xml = '\n'.join([line for line in pretty_xml.split('\n') if line.strip()])
                    out.info = "上传成功"
                    out.data = f'【key】\n{key}\n【value】\n' + pretty_xml
        return show(out, 'index') #复用模版   
    else: 
        #do something
        return redirect('/', '404:页面未找到')
    

    ############################################################################
    # finish
    ############################################################################
    return show(out)
