# -*- coding: utf-8 -*-
"""
default模块
by jimmy.dong@gmail.com 2016.1.4

注意：开发controller请以demo为参照
"""
from flask import Blueprint, render_template, abort, request, current_app, make_response
from . import *
import bucketV3 as bucket
import sqlite_db
import func_pack

controller = 'index'
blueprint = Blueprint(controller, __name__)

#action
@blueprint.route("/favicon.ico")
def favicon():
    return make_response("")

@blueprint.route("/", defaults={'action':'index'}, methods=['GET','POST'])
@blueprint.route('/<action>', methods=['GET','POST'])
def main(action):
    #init
    bucket._controller = controller
    bucket._action = action
    out = init()  # @UndefinedVariable
    out['title'] = 'IEEE WEDATA SCHEMA UPLOAD SYSTEM'
    out['headline'] = 'IEEE WEDATA SCHEMA UPLOAD SYSTEM'

    #add your code here
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
    else:
        password = ''
    if password:
        user = sqlite_db.get_user(name, password)
        if user is None:
            out.alert = "用户名/密码不正确"
        else:
            resp = redirect('/upload/', '验证通过')
            resp.set_cookie("HAMSTER", func_pack.encode_user_cookie(name, user['id']))
            return resp
            
    out.html = '''
    <form action=/ method=post>
    用户名：<input type=text name=name size=20>
    密码：<input type=password name=password size=20>
    <input type=submit value='ok'>
    </form>
    '''
    out.data = "请输入用户名和密码 (提示：本系统的用户名和密码)"
        
    #finish
    return show(out)  # @UndefinedVariable
