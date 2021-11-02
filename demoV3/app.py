# -*- coding: utf-8 -*-
""" 
DEMO: 利用Mysql UDF将Mysql数据变化存储到MongoDB
by jimmy.dong@gmail.com 2016.1.9
version 1.1
"""
import config # 加载配置文件
import bucketV3 as bucket # 加载全局变量
from flask import Flask, render_template, request, make_response, current_app
from flask_debugtoolbar import DebugToolbarExtension
from flask_uploads import configure_uploads, UploadSet
from werkzeug.utils import import_string
import logging
from logging.handlers import RotatingFileHandler
import time
import cgi
import os
import setproctitle
from job import myJob
from yepy.console import embed


#进程名称
setproctitle.setproctitle(setproctitle.getproctitle() + ' ' + config.Config.APP_NAME + ':' + str(config.Config.APP_PORT))

#The Flask Application
def createApp():
    app = Flask(__name__)
    #注册模块
    for bp_name in config.blueprints:
        bp = import_string(bp_name)
        app.register_blueprint(bp)
    #根据情况加载测试或正式配置
    if config.is_debug == True: 
        app.config.from_object(config.DevelopmentConfig)
    else:
        app.config.from_object(config.ProductionConfig)
    return app

app = createApp()

#全局变量初始化
bucket.G.begin_time = time.strftime("%Y-%m-%d %H:%M:%S")
bucket.G.counter = 0
bucket.G.counter_success = 0
#初始化核心插件
bucket.debug.start()
if app.config.get('CACHE_ENABLE'):
    bucket.cache.init_app(app, config={'CACHE_TYPE':'memcached'}) # 'simple' | 'memcached' | 'redis'
if app.config.get('DEBUG'):
    toolbar = DebugToolbarExtension(app)
if app.config.get('LOG_FILE'):
    file_handler = RotatingFileHandler(app.config['LOG_FILE'], maxBytes=app.config['LOG_SIZE'], backupCount=5)
    file_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)
photos = UploadSet(name='photos',extensions=('jpg','gif','png'))
files = UploadSet(name='files',extensions=('txt','rar','zip')) 
configure_uploads(app,(photos,files))


# Framework
@app.before_request
def before_request():
    if bucket.debug.opened():
        bucket.debug.reload()
    pass
@app.after_request
def after_request(response):
    if request.url_root.find('/static/') > -1:
        return response
    bucket.debug.time('after')
    headers = bucket.debug.show()
    if len(headers) > 0:
        for key in headers:
            response.headers[key] = headers[key]
    response.headers["Server"] = "Python/Power by YEPY %s" % config._yepy_application_version
    response.headers["Expires"] = "Expires: Mon, 26 Jul 1997 05:00:00 GMT"
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Pragma"] = "no-cache"
    return response
#@app.teardown_request
#def teardown_request():
#    pass
with app.app_context():
    pass

#上传处理
@app.route("/uploadPhoto", methods=['GET','POST'])
def uploadPhoto():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        return photos.url(filename)
    else:
        return "No photo uploaded!"
    
#异常处理
@app.errorhandler(404)
def not_found(error):
  out = repr(app.url_map)
  response = make_response('页面未找到 page not found <br/><pre>' + cgi.escape(out) + '</pre>', 404)
  return response

#临时测试
@app.route("/test")
def test():
    #print_r(bucket.mongo2.db.collection_names())
    test = bucket.mongo2.db.test
    test.insert({'test':'hello world'})
    return "Hello World!"

if __name__ == '__main__':
    #embed()
    
    #设置PID
    pid = os.getpid()
    pid_file = "app.pid"
    with open(pid_file,"w") as f:
        f.write(str(pid))
    
    #进程名称
    setproctitle.setproctitle(setproctitle.getproctitle() + ' ' + str(app.config['APP_PORT']))

    #启动工作线程
    if bucket.worker.checkStatus() == False:
        job = bucket.worker.setJob(myJob)
        job.setDaemon(True)
        job.start()
        bucket.worker.checkStatus()
        
    #启动HTTP监听
    app.run(host=app.config['APP_HOST'],port=app.config['APP_PORT'],use_reloader=app.config['USE_RELOADER'])
    
    #程序结束
    if bucket.worker.checkStatus() == 'running':
        print("warnning: worker is still not finished, force abort.")
    if(os.path.exists(pid_file)):
        os.remove(pid_file)
    print(" ---=== application finished at %s! ===---" % time.strftime("%Y-%m-%d %H:%M:%S"))
    

