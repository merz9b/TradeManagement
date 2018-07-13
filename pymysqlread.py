# -*- coding: utf-8 -*-
"""
Created on Mon May 14 09:38:47 2018

@author: Jax_GuoSen 
"""

import pymysql
import pandas as pd

#读出
def dbconn(sql_query):
    connection = pymysql.connect(host='47.100.2.112', port=33306, user='gxqh', passwd='R{Zppc7r0Lxd')
    cursor=connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql_query)
    
    data_dict=cursor.fetchall()
    connection.close
    
    col_names = list(data_dict[0].keys())
    data = pd.DataFrame(data_dict,columns=col_names)
    
    return data
