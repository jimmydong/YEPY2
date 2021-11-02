#!/bin/sh
echo "run app.py as daemon."

nohup python3.6 app.py daemon > app.log 2>&1 & echo $! > app.pid
tail -f app.log

