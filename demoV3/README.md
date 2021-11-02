# YEPY 快速开发框架项目搭建演示

本示例适用于 Python3 以上版本。 Python2.7版本请使用 demoV1 项目

本示例适用于较复杂的Web应用。如果仅需简单web页面展示运行信息，建议使用 demoV2 

## 开发指导

+ 部署YEPY代码
+ 复制demoV3到任意项目目录
+ 安装依赖 python3 setup.py install
+ 修改config.inc (留意：YEPY的路径)
+ 开发contgroller
+ 开发templates
+ 将新的controller注册到config.inc的blueprint
+ 运行 python3 app.py debug 进行调试
+ 运行 /bin/sh start.sh 正式服务

## config.inc 注意事项

+ 名称、端口
+ Cache配置（或关闭）

## job.py 

运行任务线程。可通过 bucket.G 与主程序通讯

【注意】 只能在单进程模式中唯一。如果使用gevent，每个进程中会有一个job。

## 高性能模式

wait

