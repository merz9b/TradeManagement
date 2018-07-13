# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 12:58:55 2018

@author: Harrison
"""
import PyMySQLreadZH
import pandas as pd
def GetTraderId(masterid): #获取管辖下的Id
    strall="SELECT * FROM futurexdb.client_terminal where roletype=%s;"%masterid
    a=PyMySQLreadZH.dbconn(strall)
    return a

#%%使用方法
if __name__ == '__main__':
    a=GetTraderId('12')
    trade_id = a['accountid'].tolist()
    
