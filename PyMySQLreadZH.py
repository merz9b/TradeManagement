# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 13:07:17 2018

@author: Harrison
"""

import pymysql
import pandas as pd
#%% 接口：单纯读取MySQL表单数据
def dbconn(sql_query):
    connection = pymysql.connect(host='47.100.2.112', port=33306, user='gxqh', passwd='R{Zppc7r0Lxd',charset='utf8')
    cursor=connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql_query)
    data_dict=cursor.fetchall()
    connection.close
    col_names = list(data_dict[0].keys())
    data = pd.DataFrame(data_dict,columns=col_names)
    return data

def readexchangeZH(exchange):
    strall="SELECT * FROM futurexdb.exchange where symbol='"+exchange+"';"
    ZH=dbconn(strall)
    namezh=ZH.desc_zh[0]
    return namezh

def readcontructZH(exchange,underlingname):
    strall="SELECT * FROM futurexdb.underlying where exchange_symbol='"+exchange+"'and underlying_symbol='"+underlingname+"';"
    ZH=dbconn(strall)
    namezh=ZH.desc_zh[0]
    return namezh