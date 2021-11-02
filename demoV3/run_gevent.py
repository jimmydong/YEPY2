#coding=utf-8
#!/usr/bin/python

#
# 运行需求：
# pip2.7 install gevent
# pip2.7 install setproctitle
#
import config # 加载配置文件
import bucketV3 as bucket # 加载全局变量
from app import app # 加载APP
import os
import time
import setproctitle
from gevent.wsgi import WSGIServer

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
http_server = WSGIServer(('', config.Config.APP_PORT), app)
try:
    http_server.serve_forever()
except KeyboardInterrupt:
    pass
#程序结束
if(os.path.exists(pid_file)):
    os.remove(pid_file)
print(" ---=== application finished at %s! ===---" % time.strftime("%Y-%m-%d %H:%M:%S"))
