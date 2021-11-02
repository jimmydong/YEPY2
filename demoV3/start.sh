#!/bin/sh
/usr/bin/nohup /usr/local/bin/python3 run_gevent.py >> log/access.log 2>&1 &
