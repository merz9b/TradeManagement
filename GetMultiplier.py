# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 14:02:41 2018

@author: Jax_GuoSen
"""

import PyMySQLreadZH
#%%获取角色列表
def GetMultiplier(symbol):
    strall="SELECT * FROM futurexdb.underlying where underlying_symbol='"+symbol+"';"
    a=PyMySQLreadZH.dbconn(strall)
    return a
#%%使用方法
if __name__ == '__main__':
    a=GetMultiplier('rb')
    idlist1=a.multiplier