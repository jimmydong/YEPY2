# -*- coding: utf-8 -*-
'''
本地sqlite文件操作封装
'''
import sqlite3
import os
import time

sqlite_db_file = os.path.dirname(os.path.dirname(__file__)) + '/sqlite.db' #数据库文件
        
#     # 更新数据
#     update_sql = "UPDATE users SET age = ? WHERE name = ?"
#     cursor.execute(update_sql, (31, "张三"))
#     conn.commit()
#     print("\n数据更新成功")

# 数据字典
def row_factory(cursor, row):
    data = {}
    for idx, col in enumerate(cursor.description):
        data[col[0]] = row[idx]
    return data

# 查找用户
def get_user(name, password):
    try:
        conn = sqlite3.connect(sqlite_db_file)
        #conn.row_factory = lambda cursor, row: {key: value for key, value in zip([column[0] for column in cursor.description], row)}
        conn.row_factory = row_factory
        sql_pre = "SELECT * FROM user WHERE name=? AND password=?"
        sql_data = (name, password)
        res = conn.execute(sql_pre, sql_data)
        data = res.fetchone()
        #print(data)
        return data
    except sqlite3.Error as e:
        print(f"数据库操作出错: {e}")
    finally:
        if conn:
            conn.close()
    return None

# 插入数据
def insert_upload(user_id, business_id, structure, redis_key, redis_value, xml_filename, xml_data):
    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    try:
        conn = sqlite3.connect(sqlite_db_file)
        sql_pre = "INSERT INTO upload (user_id, business_id, datetime, structure, redis_key, redis_value, xml_filename, xml_data) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        sql_data = (user_id, business_id, datetime, structure, redis_key, redis_value, xml_filename, xml_data)
        conn.execute(sql_pre, sql_data)
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"数据库操作出错: {e}")
    finally:
        if conn:
            conn.close()
    return None

# 读取列表
def list_upload(start = 0, limit = 100):
    try:
        conn = sqlite3.connect(sqlite_db_file)
        conn.row_factory = row_factory
        sql_pre = "SELECT upload.*, user.name FROM upload LEFT JOIN user ON upload.user_id = user.id ORDER BY id DESC LIMIT ?, ?"
        sql_data = (start, limit)
        res = conn.execute(sql_pre, sql_data)
        rows = res.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"数据库操作出错: {e}")
    finally:
        if conn:
            conn.close()
    return None

# 用ID获取upload
def get_upload(id):
    try:
        conn = sqlite3.connect(sqlite_db_file)
        conn.row_factory = row_factory
        sql_pre = "SELECT * FROM upload WHERE id=?"
        sql_data = (id)
        res = conn.execute(sql_pre, sql_data)
        data = res.fetchone()
        return data
    except sqlite3.Error as e:
        print(f"数据库操作出错: {e}")
    finally:
        if conn:
            conn.close()
    return None


