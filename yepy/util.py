# -*- coding: utf-8 -*-
"""
YEPY 常用工具模块
by jimmy.dong@gmail.com 2018.10.19
"""
import sys
import time
import json

class Debug:
    
    def __init__(self):
        pass
            
    def json_ok(self, data, msg="success"):
        '''json输出'''
        result = {
            "success": True,
            "msg": msg,
            "data": data or ""
        }
        if type(msg) is unicode:    # @UndefinedVariable
            result["msg"] = msg.encode("utf-8")
    
        return json.dumps(result)

    def json_fail(self, msg="Failed"):
        '''json输出'''
        result = {
            "success": False,
            "msg": msg,
            "data": ""
        }
        if type(msg) is unicode:    # @UndefinedVariable
            result["msg"] = msg.encode("utf-8")
    
        return json.dumps(result)

