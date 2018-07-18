# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 09:27:03 2018

@author: Harrison
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'HaiFeng'
__mtime__ = '2016/9/13'
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
	def q_OnFrontConnected(self):
		print('connected')
		self.q.ReqUserLogin(BrokerID=self.broker, UserID=self.investor, Password=self.pwd)

	def q_OnRspUserLogin(self, rsp, info, req, last):
		#print(info)

		#insts = create_string_buffer(b'cu', 5)
		self.q.SubscribeMarketData('rb1901')
		self.q.SubscribeMarketData('hc1901')
	def q_OnTick(self, tick):
		#print('-----------------------------------')
		self.ff = CThostFtdcMarketDataField()
		self.ff = tick
		#print(self.ff.LastPrice,self.ff.InstrumentID)
		#print(time.time(),self.a)

		if time.time()-self.a>3:
				b=self.ff.LastPrice 
				c=self.ff.InstrumentID
				self.a=time.time()
				print(b,c)  
		
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
		#self.q.Join()
 
if __name__ == '__main__':
	t = Test()
	a=t.StartQuote()    
    