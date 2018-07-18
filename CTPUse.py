# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 14:16:35 2018

@author: Harrison
"""

import sys
import os
sys.path.append(os.path.join(sys.path[0], '..'))	 #调用父目录下的模块

from py_ctp.ctp_struct import *
from py_ctp.trade import Trade
from py_ctp.quote import Quote
import _thread
from time import sleep
import time
import pandas as pd
import tkinter

class Test:

    def __init__(self):
        self.Session = ''
        self.q = Quote()
        self.t = Trade()
        self.req = 0
        self.ordered = False
        self.needAuth = False
        self.RelogEnable = True
        self.ff = CThostFtdcMarketDataField()
        self.a=time.time()
        self.datas=pd.DataFrame(columns=['code','price','time'])
        #self.codelist=['rb1901','hc1901','m1901','c1901','i1901','CF809','AP807','ru1809','ru1808','rb1809']
        #self.datas.loc[time.time(),['code','price']]=['a',0]
        self.datas['code']=self.codelist
        self.datas['price']=0
        self.datas['time']=time.time()
        
        
        
        #self.root = tkinter.Tk()
        #self.t = tkinter.Text(self.root)
        #self.t.pack(expand=1, fill='both')
        
        
        
    def q_OnFrontConnected(self):
        print('connected')
        self.q.ReqUserLogin(BrokerID=self.broker, UserID=self.investor, Password=self.pwd)

    def q_OnRspUserLogin(self, rsp, info, req, last):
        #print(info)

        #insts = create_string_buffer(b'cu', 5)
        for i in range(len(self.codelist)):
            self.q.SubscribeMarketData(self.codelist[i])
    def q_OnTick(self, tick):
        #print('-----------------------------------')
        self.ff = CThostFtdcMarketDataField()
        self.ff = tick
        #print(self.ff.LastPrice,self.ff.InstrumentID)
        #print(time.time(),self.a)
        
        timeb=time.time()
        timec=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        #if timea-self.a>3:
            #self.datas.loc[timea,['code','price']]=[self.ff.getInstrumentID(),self.ff.getLastPrice()]
        self.datas.loc[self.datas['code']==self.ff.getInstrumentID(),['price','time']]=[self.ff.getLastPrice(),timec]
        #print(timec)
        if timeb-self.a>5:
            self.datab=self.datas
            self.a=timeb
            print(self.datab)
    #        _thread.start_new_thread(self.tik,())
      

    #def tik(self):  

    #    print(11111111)

		
    def OnFrontConnected(self):
        if not self.RelogEnable:
            return
        print('connected')
        if self.needAuth:
            self.t.ReqAuthenticate(self.broker, self.investor, '@haifeng', '8MTL59FK1QGLKQW2')
        else:
            self.t.ReqUserLogin(BrokerID=self.broker, UserID=self.investor, Password=self.pwd, UserProductInfo='@haifeng')

    def OnRspAuthenticate(self, pRspAuthenticateField=CThostFtdcRspAuthenticateField, pRspInfo=CThostFtdcRspInfoField, nRequestID=int, bIsLast=bool):
        print('auth：{0}:{1}'.format(pRspInfo.getErrorID(), pRspInfo.getErrorMsg()))
        self.t.ReqUserLogin(BrokerID=self.broker, UserID=self.investor, Password=self.pwd, UserProductInfo='@haifeng')

    def OnRspUserLogin(self, rsp, info, req, last):
        i = CThostFtdcRspInfoField()
        i = info
        #print(i.getErrorMsg())
    
        if i.getErrorID() == 0:
            self.Session = rsp.getSessionID()
            self.t.ReqSettlementInfoConfirm(BrokerID = self.broker, InvestorID = self.investor)
        else:
            self.RelogEnable = False

    def StartQuote(self):
        self.frontAddr = 'tcp://101.231.162.58:41213,tcp://101.231.162.59:41213'
        self.broker = '6000'
        self.investor = ''
        self.pwd = ''
            
        api = self.q.CreateApi()
        spi = self.q.CreateSpi()
        self.q.RegisterSpi(spi)
    
        self.q.OnFrontConnected = self.q_OnFrontConnected
        self.q.OnRspUserLogin = self.q_OnRspUserLogin
        self.q.OnRtnDepthMarketData = self.q_OnTick
    
        self.q.RegCB()
    
        self.q.RegisterFront(self.frontAddr.split(',')[0])
        self.q.Init()
        self.root.mainloop()
        #self.q.Join()
 
if __name__ == '__main__':
    t = Test()
    t.StartQuote()    
    