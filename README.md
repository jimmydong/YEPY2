# YEPY - Yep! Easy Python

It's very small web framework for python. Current version is 0.01beta.

If you want join us, mailto://jimmy.dong@gmail.com

## Prepare:

	$ pip install [logging flask flask-debugtoolbar flask-uploads flask-cache flask-pymongo flask-sqlalchemy python-memcached pymongo SQLAlchemy yapf 

推荐安装： ipython（jupiter）

	
## Usage:

copy demo/*  to your project folder as a new project

edit config.py to config site parameters,

create your controller according to controller/demo.py, edit config.py to regist new controller

create your model and templates as your need

run:

	python application.py   --- windows 
	or
	$/bin/sh start.sh  --- linux
	
## Patch JDPT

copy patch/jdpt.py to %python_lib_path%/

add followings to %python_lib_path%/site.py

```
######################################################################
#  hack JDPT
import jdpt
######################################################################
```

Test
----

## 关于项目DEMO

### demoV1 

	适用于python2.x版本。已停止维护，不建议使用。
	
### demoV2

	python3.x
	
	适用于业务逻辑处理为主的小型项目
	
	配置与主程序分开
	
	业务逻辑请放在 run 中
	
	直接运行，为执行一次 run 的业务逻辑
	
	加参数 daemon ， 会定时执行 run ，并且启动一个轻量 http-server， 用以查看运行状况
	
### demoV3

	python3.x
	
	适用于网页交互为主的项目
	
	controller/action/template 分离
	
	请认真修改 config 中配置项
	
	支持页面调试和firephp调试
	
	支持全局变量传递
	
	支持 worker 线程
	
	具体开发步骤，请参见 demoV3 下 README.md
	
	