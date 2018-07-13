# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 13:40:19 2018

@author: Harrison
"""
import PyMySQLreadZH
#%%获取角色列表
def GetRoleType(roletype):
    strall="SELECT * FROM futurexdb.client_terminal where roletype="+roletype+";"
    a=PyMySQLreadZH.dbconn(strall)
    return a
#%%使用方法
if __name__ == '__main__':
    a=GetRoleType('11')
    idlist1=a.accountid
    b=GetRoleType('13')
    idlist2=b.accountid