# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 10:33:04 2018

@author: Jax_GuoSen
"""

import PyMySQLreadZH
import pandas as pd
def GetPortDetail(portfolio_symbol,traderid): #获取管辖下的Id
    strall="SELECT * FROM futurexdb.order_record_otc where portfolio_symbol = '%s' and traderid = %d and status=1;"%(portfolio_symbol,traderid)
    a=PyMySQLreadZH.dbconn(strall)
    return a

#%%
def GetPortDetail2(orderid):
    strall = "SELECT * FROM futurexdb.model_params where modelinstance = '%s';"%orderid
    a=PyMySQLreadZH.dbconn(strall)
    return a
def GetPortSub():
    strall =" SELECT * FROM futurexdb.model_params where model in('oao','ovo')and paramname='ref_contract' ;"
    a=PyMySQLreadZH.dbconn(strall)
    a = a['paramstring'].drop_duplicates().tolist()
    return a
#%%使用方法
if __name__ == '__main__':
    a = GetPortDetail('OTC_DCE-m',12001)
    print(a)
    b = GetPortDetail2('ovo_13001_11005_1533174873.6223238')
    print(b)