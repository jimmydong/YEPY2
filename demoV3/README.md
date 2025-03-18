# wedata实现IEGG非标kafka数据源schema evaluation

### install

    pip3 install redis
    pip3 install flask_debugtoolbar
    pip3 install flask_uploads
    pip3 install wxpy
    pip3 install setproctitle
    pip3 install tornado
    mkdir log

## database
    pip3 install sqlite_web
    sqlite_web 

### patch

/Users/laodong/Library/Python/3.9/lib/python/site-packages/flask_uploads.py (具体路径看报错提示)

Change

    from werkzeug import secure_filename,FileStorage

to

    from werkzeug.utils import secure_filename
    from werkzeug.datastructures import  FileStorage

### run

    python3 app.py
    #or
    sh start.sh


### deployment

    http://http://gdit-sre-console.deltaverse-intl.com:27788

