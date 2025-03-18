#!/bin/sh
/usr/bin/nohup python3 run_tornado.py > log/access.log 2>&1 &
