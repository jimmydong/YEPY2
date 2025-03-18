# -*- coding: utf-8 -*-
"""
YEPY 控制器模块
by jimmy.dong@gmail.com

增加控制器的步骤：
1，新建xxxx.py
2，修改config.py[核心配置]，注册新控制器
"""
from flask import Blueprint, render_template, abort, request, current_app, make_response
from jinja2 import TemplateNotFound
import bucketV3 as bucket
_yepy_controller_version = '1.0b'

def init():
    # init before action
    out = bucket.ConfigG()
    return out

def show(out, template = None):
    # show after action
    try:
        if template:
            if isinstance(template, tuple):
                response = make_response(render_template('%s/%s.html' % template, out=out))
            else:
                response = make_response(render_template('%s/%s.html' % (bucket._controller, template), out=out))
        elif bucket._controller == 'index':
            response = make_response(render_template('%s.html' % (bucket._action), out=out))
        else:
            response = make_response(render_template('%s/%s.html' % (bucket._controller,bucket._action), out=out))
        return response
    except TemplateNotFound:
        abort(404)

def redirect(url, title = '请稍候', body = '页面跳转中，请稍候...'):
    # redirect to url
    html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <meta http-equiv="refresh" content="1; url={url}" />
            <title>{title}</title>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
            <link rel="stylesheet" href="/static/laodong.css">
            <script src="https://code.jquery.com/jquery-1.12.4.min.js" integrity="sha256-ZosEbRLbNQzLpnKIkEdrPv7lOy9C27hHQ+Xp8a4MxAQ=" crossorigin="anonymous"></script>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
        </head>
        <body>
        <div style="height: 400px;width: 100%;display: flex;justify-content: center;align-items: center;">
            <div class="mb-3">{body}</div>
        </div>
        </body>
        <script>
        setTimeout(function(){{
            window.location.href = '{url}'
        }}, 500)
        </script>
        </html>
    '''
    return make_response(html)

def error(url, title = '错误', body = '结果错误，请返回进行检查'):
    # redirect to url
    html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <title>{title}</title>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
            <link rel="stylesheet" href="/static/laodong.css">
            <script src="https://code.jquery.com/jquery-1.12.4.min.js" integrity="sha256-ZosEbRLbNQzLpnKIkEdrPv7lOy9C27hHQ+Xp8a4MxAQ=" crossorigin="anonymous"></script>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
        </head>
        <body>
        <div style="height: 400px;width: 100%;display: flex;justify-content: center;align-items: center;">
            <div class="mb-3">{body}</div>
            <div class="mb-3"><button type="button" class="btn btn-danger" onclick="window.location.href = '{url}'">返回</button></div>
        </div>
        </body>
        <script>
        setTimeout(function(){{
            window.location.href = '{url}'
        }}, 9000)
        </script>
        </html>
    '''
    return make_response(html)


