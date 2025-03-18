
# -*- coding: utf-8 -*-
'''
将XML文件中目标struct提取出来，上传到Redis
'''
import redis
import xml.etree.ElementTree as ET
from pprint import pprint

redis_host = "bj-crs-djw4zifj.sql.tencentcdb.com"
redis_port = 21176
redis_password = 'iegg@Wedata@2022'

# 提取XML子结构
def get_struct(root, struct_name):
    #print(f"get_struct: {struct_name}")
    # 使用XPath查找目标struct元素
    struct = root.find(f".//struct[@name='{struct_name}']")
    if struct is None:
        print(f'没有找到子结构(可能是需要补充的类型): {struct_name}')
        return None
    re = ET.Element('struct', struct.attrib)
    # 检查是否有嵌套
    for i in struct:
        if i.tag != 'entry':
            print(f'未知的元素: {i}')
        for k in i.attrib:
            if k == 'type' and i.attrib[k] not in ['string', 'int', 'bigint', 'datetime', 'usmallint', 'biguint', 'smallint', 'float']:
                sub_struct = get_struct(root, i.attrib[k])
                if sub_struct is None:
                    re.append(i) #可能是未配置的type，按常规处理
                    continue
                else:
                    for ii in sub_struct:
                        re.append(ii) #将子结构中的字段逐个加入
                    continue
        re.append(i)  
    return re

# 处理XML内容
def handle_xml(xml_string, bid, table):
    root = ET.fromstring(xml_string)

    target_struct = get_struct(root, table)
    if target_struct is None:
        print(f'文件中未找到结构 {table}')
        return None, None
    
    key = f'{bid}:{table}'
    value = ET.tostring(target_struct, encoding='utf-8', xml_declaration=True)
    
    # 更新至Redis
    #ret = redis_set(key, value)
    # if not ret:
    #     return None, None
    
    # 保存到文件
    #new_tree = ET.ElementTree(target_struct)
    #new_tree.write('upload.xml', encoding='utf-8', xml_declaration=True)

    # TODO::保存到数据库
    # 
    
    return key, value

# 写入redis
def redis_set(key, value):
    try:
        # 创建Redis连接
        r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password) 
        # 测试连接
        if not r.ping():
            raise ConnectionError("Redis连接失败")
        r.set(key, value)
        # print(key)
        # print(str(r.get(key), encoding='utf-8'))
        return True
    except redis.exceptions.AuthenticationError:
        print("认证失败，请检查用户名/密码")
    except redis.exceptions.ConnectionError:
        print("连接失败，请检查地址/端口/网络连接")
    except Exception as e:
        print(f"操作异常：{str(e)}")
    return False

# 读取redis
def redis_get(key):
    try:
        # 创建Redis连接
        r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password) 
        # 测试连接
        if not r.ping():
            raise ConnectionError("Redis连接失败")
        ret = r.get(key)
        return ret
    except redis.exceptions.AuthenticationError:
        print("认证失败，请检查用户名/密码")
    except redis.exceptions.ConnectionError:
        print("连接失败，请检查地址/端口/网络连接")
    except Exception as e:
        print(f"操作异常：{str(e)}")
    return False

if __name__ == "__main__":
    # xml_file = '/Users/laodong/Downloads/g_ieg_dny_itop_rule_engine_prod.xml'
    # bid = 'g_ieg_dny_itop_rule_engine_prod'
    # table = 'RuleEngineSensitiveOpProd'
    # with open(xml_file, 'r') as f:
    #     parse_xml(f.read(), bid, table)

    # xml_file = '/Users/laodong/Downloads/g_ieg_dny_pubgmitop.xml'
    # bid = 'g_ieg_dny_pubgmitop'
    # table = 'iMSDKAPILog'
    # with open(xml_file, 'r') as f:
    #     parse_xml(f.read(), bid, table)

    #这是一个包含公共字段的实例
    xml_file = '/Users/laodong/Downloads/tdm_sg.xml'
    bid = 'tdm_sg'
    table = 'insight_220827193_100_xrstore_search_hotWord'
    with open(xml_file, 'r') as f:
        string = f.read()
        #print(string)
        handle_xml(string, bid, table)
    