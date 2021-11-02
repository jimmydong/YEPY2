# -*- coding: utf-8 -*-
'''
APP + 简易HTTP

适用于开发简单功能，配合HTTP可远程查看日志。例如： 守护狗等

运行方式：

1， 只执行一次  

    python3 app.py

2， 守护运行

    python3 app.py daemon


'''
import sys
import io
import shutil
from threading import Timer
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib
import logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S')
import config
import json
from yepy.http_helper import CreateHtmlClass
ct_obj = CreateHtmlClass()
from yepy.console import embed

counter = 0

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.process('get')
        
    def do_POST(self):
        self.process('post')
    
    def process(self, method):
        
        # 处理静态资源文件
        query_file = self.path.split('?',1)[0]
        if query_file != '/':
            err_code,content_type,content = ct_obj.root_html(query_file)
            self.send_response(err_code)
            self.send_header("Content-type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return

        # 处理参数
        params = {}
        if method == 'post':
            postData=self.rfile.read(int(self.headers['content-length']))
            params=urllib.parse.parse_qs(postData.decode())
        elif method == 'get':
            if '?' in self.path:
                queryString=urllib.parse.unquote(self.path.split('?',1)[1])
                params=urllib.parse.parse_qs(queryString)
        else:
            pass
        
        # 注意： 每个参数都是[]
        logging.debug(params)
        if params.get('_c') == ['exit']:
            print('exit ...')
            out = 'exit ... Done!'
            self.wfile.write(out.encode('UTF-8'))
            exit()
        
        out = "<h1>Hello world! " + str(counter) + "</h1><a href='/?_c=exit'>exit</a><br/><a href='/?_c=demo&_a=check&msg=哈哈'>test get</a>  <form method=post action='/'><input type=hidden name=_c value='doPost'><input type=hidden name=_a value='check'><input type=hidden name=chinese value='中文测试'><input type=submit value='test post'></form> 参数：<hr/>"
        out = out + "<pre>" + json.dumps(params, ensure_ascii=False) + "</pre><hr/><img src='test.jpg'/>"
        
        content = out.encode(encoding='UTF-8')
        self.send_response(200)     
        self.send_header("Content-type", "text/html; charset=UTF-8")
        self.send_header("Content-Length",str(len(content)))
        self.end_headers()
        self.wfile.write(content)

def run():
    global counter
    logging.debug('这里是主处理逻辑 ' + str(counter))
    counter += 1

# 守护模式运行
def daemon(second):
    run()
    second += 5
    t = Timer(second, daemon, (second,))
    t.setDaemon(True)
    t.start()
    
if __name__ == '__main__':
    #命令行参数处理
    if len(sys.argv) > 1:
        if sys.argv[1] == 'daemon':
            #守护运行
            t = Timer(config.run_percecond, daemon, (config.run_percecond,))
            t.setDaemon(True)
            t.start()
        server_address = ('', config.http_port)
        httpd = HTTPServer(server_address, MyRequestHandler)
        logging.debug("serving at port: " + str(config.http_port))
        httpd.serve_forever()
    else:
        run()
        