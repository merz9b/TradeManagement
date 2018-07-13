# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 09:46:29 2018

@author: Harrison
"""
import PyMySQLreadZH
def GetPoSymbol(traderid): #获取管辖下的Id
    strall="SELECT * FROM futurexdb.portfolio where accountid='"+traderid+"';"
    a=PyMySQLreadZH.dbconn(strall)
    return a
if __name__ == '__main__':
    a=GetPoSymbol('12001')
    a.portfolio_symbol[0]