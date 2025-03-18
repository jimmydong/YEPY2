#coding=utf-8
#!/usr/bin/python3

import config # 加载配置文件
from app import app # 加载APP
import os
import time
import setproctitle
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from tornado.web import FallbackHandler, RequestHandler, Application

class MainHandler(RequestHandler):
  def get(self):
    self.write("This message comes from Tornado ^_^")

if __name__ == "__main__":
    #进程名称
    setproctitle.setproctitle(setproctitle.getproctitle() + ' ' + config.Config.APP_NAME)
    #设置PID
    pid_file = "application.pid"
    pid = os.getpid()
    with open(pid_file, 'w') as f:
        f.write(str(pid))
    #设置非调试模式
    os.environ['MODE'] = 'PRODUCTION'
    #启动监听  
    application = Application([
        (r"/tornado", MainHandler),
        (r".*", FallbackHandler, dict(fallback=WSGIContainer(app))),
    ])
    application.listen(config.Config.APP_PORT)
    print(" ---=== application listen port: %s ===---" % config.Config.APP_PORT)
    try:
        IOLoop.instance().start()
    except KeyboardInterrupt:
        pass

    #程序结束
    if(os.path.exists(pid_file)):
        os.remove(pid_file)
    print(" ---=== application finished at %s! ===---" % time.strftime("%Y-%m-%d %H:%M:%S"))
