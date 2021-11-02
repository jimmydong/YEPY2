# -*- coding: utf-8 -*-
import bucketV3 as bucket

class MyRecord():
    message = ''
    created = 0
    levelname = ''
    pathname = ''
    lineno = 0
    def getMessage(self):
        return self.message

class MyRecordHandler():
    data = []
    def get_records(self):
        return self.data
    def clear_records(self):
        self.data = []
        return True
    def add_record(self, levelname, created, message, pathname, lineno):
        t = MyRecord()
        t.message = message
        t.created = created
        t.levelname = levelname
        t.pathname = pathname
        t.lineno = lineno
        self.data.append(t)
        return True
        