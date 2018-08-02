# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 14:45:48 2018

@author: Jax_GuoSen
"""

from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import TimeSeriesInterpolator
import GetTraderId
import GetPoSymbol
import numpy as np
import pandas as pd
import GetPortDetail
import datetime
import Greeks
import OptionPricer
import GetMultiplier
import Tprice_RealTime
import CTPUse
from py_ctp.quote import Quote
from py_ctp.ctp_struct import *
import time
import _thread
class Application(CTPUse.Test):
    def __init__(self):
        #construct a UI
        self.Session = ''
        self.q = Quote()
        self.req = 0
        self.ordered = False
        self.needAuth = False
        self.RelogEnable = True
        self.ff = CThostFtdcMarketDataField()
        self.a=time.time()
        self.datas=pd.DataFrame(columns=['code','price','time'])
        self.codelist=GetPortDetail.GetPortSub()
        #self.datas.loc[time.time(),['code','price']]=['a',0]
        self.datas['code']=self.codelist
        self.datas['price']=0
        self.datas['time']=time.time()
        self.datab=self.datas
        self.q = Quote()
        self.root = Tk()
        self.root.title('国信期货衍生品风险管理界面')
    
    def init_widgets(self):
        labelframe1 = LabelFrame(self.root, text='Login')
        labelframe1.pack(fill='y',side='left',expand=False)
        
        self.TraderChosen = ttk.Combobox(labelframe1, width=12)
        TraderID = GetTraderId.GetTraderId('12')
        TraderID = TraderID['accountid'].tolist()
        self.TraderChosen['values'] =  TraderID
        self.TraderChosen.pack(fill='both')
        self.TraderChosen.bind("<<ComboboxSelected>>",self.select_portfolio_symbol)
    
        self.PortfolioChosen = ttk.Combobox(labelframe1, width=12)
        self.PortfolioChosen.pack(fill='both')
        
        self.PortfolioChosen.bind("<<ComboboxSelected>>",self.UpdateDataA)
        button_bg = '#D5E0EE'  
        button_active_bg = '#E5E35B'
        bt = Button(labelframe1,text='UpdateData',bg=button_bg, padx=50, pady=3,fg='green',\
                    command=lambda : self.UpdateDataOrigin(),activebackground = button_active_bg,\
                    font = tkFont.Font(size=12, weight=tkFont.BOLD))
        bt.pack(fill='both')
        
        bt = Button(labelframe1,text='Calculate_Vol',bg=button_bg, padx=50, pady=3,fg='red',\
                    command=lambda : self.create_vol_widgets(),activebackground = button_active_bg,\
                    font = tkFont.Font(size=12, weight=tkFont.BOLD))
        bt.pack(fill='both')
        
        bt = Button(labelframe1,text='Calculate_Greeks',bg=button_bg, padx=50, pady=3,fg='red',\
                    command=lambda : self.create_greeks_widgets(),activebackground = button_active_bg,\
                    font = tkFont.Font(size=12, weight=tkFont.BOLD))
        bt.pack(fill='both')
        



    def select_portfolio_symbol(self,event):
        a = GetPoSymbol.GetPoSymbol(self.TraderChosen.get())
        portfolio_lst = a.portfolio_symbol.tolist()
        self.PortfolioChosen['values'] = portfolio_lst
        self.PortfolioChosen.current(0)
        self.UpdateData()              #初始开启自动循环
    def UpdateDataOrigin(self):
        #删除原先的集合
        self.vol_lst = []
        self.clear(self.sec_sub_dict)
        self.clear(self.sec_sub_dict_greeks)
        self.clear(self.sec_sub_dict_vol)
        
        info1 = GetPortDetail.GetPortDetail(self.PortfolioChosen.get(),int(self.TraderChosen.get()))
        self.info_greeks = []
        self.box = []
        self.info_vol = []
        
        for i in range(len(info1)):
            info2 = GetPortDetail.GetPortDetail2(info1.loc[i,'modelinstance'])
            current_date = datetime.datetime.now().date()
            end_date = info2[info2['paramname']=='exp_date']['paramstring'].values[0]
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
            underlying = info2[info2['paramname']=='ref_underlying']['paramstring'].values[0]
            exchange = info2[info2['paramname']=='ref_exchange']['paramstring'].values[0]
            contract_name = exchange+'_'+info2[info2['paramname']=='ref_contract']['paramstring'].values[0]
            
            contract = str.lower(info2[info2['paramname']=='ref_contract']['paramstring'].values[0])
            if not contract[-4].isdigit():
                contract = str.upper(contract)
                
            multiplier = GetMultiplier.GetMultiplier(underlying)['multiplier'].values[0]
            
            #print(multiplier)
            #print(type(multiplier))
            
            if end_date>current_date:
                tmp = {'ContractName':contract_name,\
                       'Strike':info2[info2['paramname']=='strike']['paramstring'].values[0],\
                       'TTM(days)':(end_date-current_date).days,\
                       'Type':info1.loc[i,'modelinstance'][:3],\
                       'DealVol':info1.loc[i,'theo_volatility'],\
                       'Rf':info1.loc[i,'riskfree_rate'],\
                       'OptionType':'call' if info2[info2['paramname']=='option_type']['paramstring'].values[0]=='0' else 'put',\
                       'HistoricalAvg':info2[info2['paramname']=='strike']['paramstring'].values[0],\
                       'CurrentPrice':self.datab[self.datab['code']==contract]['price'].values[0],\
                       'Quantity':info1.loc[i,'quantity'],\
                       'Multiplier':multiplier,\
                       'Exchange':exchange,\
                       'Underlying':underlying,\
                       'is_buy':info1.loc[i,'is_buy']}
                tmp['Type'] = tmp['Type']+'_'+tmp['OptionType']
                
                
                box_tmp = self.create_widgets(tmp)
                
                if tmp['Type'][:3] == 'oao':
                    d1 = info2[info2['paramname']=='sett_start_date']['paramstring'].values[0]
                    d1 = datetime.datetime.strptime(d1, "%Y-%m-%d").date()
                    d2 = info2[info2['paramname']=='sett_end_date']['paramstring'].values[0]
                    d2 = datetime.datetime.strptime(d2, "%Y-%m-%d").date()
                    self.info_greeks.append([tmp['Strike'],current_date,end_date,d1,d2,tmp['DealVol'],\
                                             tmp['Rf'],tmp['Type'],tmp['OptionType'],tmp['Quantity'],\
                                             tmp['Multiplier']])
                    self.info_vol.append([tmp['Exchange'],tmp['Underlying'],float(tmp['TTM(days)']),[float(tmp['Strike'])],tmp['is_buy']])
                    
                elif tmp['Type'][:3] == 'ovo':
                    self.info_greeks.append([tmp['Strike'],current_date,end_date,'','',tmp['DealVol'],\
                                             tmp['Rf'],tmp['Type'],tmp['OptionType'],tmp['Quantity'],\
                                             tmp['Multiplier'],tmp['is_buy']])
    
                    self.info_vol.append([tmp['Exchange'],tmp['Underlying'],tmp['TTM(days)'],[float(tmp['Strike'])],tmp['is_buy']])
                    #print(type(tmp['is_buy']))
                else:
                    pass
                self.box.append(box_tmp)
            else:
                pass
        #print(self.info_greeks,self.box)
        self.create_vol_widgets()
        self.create_greeks_widgets() 
        print('===============================')
        print('更新CTP价格数据')
        print(self.datab)
        print('===============================')
    def UpdateDataA(self,event):
        self.UpdateDataOrigin()
        
    def UpdateData(self):
        self.UpdateDataOrigin()
        self.root.after(150000, self.UpdateData)
        
    def create_section(self):
        self.sec3 = LabelFrame(self.root, text='Greeks')
        self.sec3.pack(fill='y',side='right')
        self.sec4 = LabelFrame(self.root, text='Current_Vol')
        self.sec4.pack(fill='y',side='right')
        self.sec2 = LabelFrame(self.root, text='Parameters')
        self.sec2.pack(fill='y',side='right')
        self.sec1 = LabelFrame(self.root, text='Contract')
        self.sec1.pack(fill='y',side='right')



        
        
        sec_sub = {'sec1':['ContractName'],'sec2':['Strike','TTM(days)','Type',\
                   'Rf','Quantity','Multiplier','HistoricalAvg','CurrentPrice','DealVol'],\
                   'sec3':['Delta','Gamma','Vega(%)','ThetaPerday','Rho(%)'],\
                   'sec4':['QuantVol']}
        self.sec_sub_dict = {}
        self.sec_sub_dict_greeks = {}
        self.sec_sub_dict_vol = {}
        for sec in ['sec1','sec2']:
            for each in sec_sub[sec]:
                l = LabelFrame(eval('self.'+sec),text = each)
                l.pack(fill='y',side='left')
                self.sec_sub_dict.update({each:l})
                
        for each in sec_sub['sec3']:
                l = LabelFrame(self.sec3,text = each)
                l.pack(fill='y',side='left')
                self.sec_sub_dict_greeks.update({each:l})
                
        for each in sec_sub['sec4']:
                l = LabelFrame(self.sec4,text = each)
                l.pack(fill='y',side='left')
                self.sec_sub_dict_vol.update({each:l})
       # _thread.start_new_thread(self.UpdateAAA,())
    def create_widgets(self,value):
        box = {}
        for each in list(self.sec_sub_dict.keys()):
            if each in ['HistoricalAvg','CurrentPrice']:
                sb = Spinbox(self.sec_sub_dict[each],from_=0,to=100000000,increment=1,width=10)
                sb.pack(fill='x',side='top')
                sb.delete(0, END)
                sb.insert(0,value[each])
                box.update({each:sb})
            else:
                lb = Label(self.sec_sub_dict[each],width=10)
                lb.pack(fill='x',side='top')
                lb.config(text=str(value[each]))
                #self.box.update({each:lb})
        return box   

    def clear(self,box):
        for slaves in list(box.values()):
            former = slaves.pack_slaves()
            for each in former:
                each.destroy()
    
    def create_greeks_widgets(self):
        res = self.cal_greeks()
        res_total = {'Delta':0,
               'Gamma':0,
               'Vega(%)':0,
               'ThetaPerday':0,
               'Rho(%)':0     
               }
        #print(res)
        self.clear(self.sec_sub_dict_greeks)
                
        for i in range(len(res)):
            for each in list(self.sec_sub_dict_greeks.keys()):
                direction = -1 if self.info_greeks[i][11] == 1 else 1
                TrueValue = res[i][each]*self.info_greeks[i][9]*self.info_greeks[i][10]*direction
                TrueValue = round(TrueValue,3)
                color = 'red' if TrueValue>=0 else 'green'
                res_total[each] = res_total[each]+TrueValue
                lb = Label(self.sec_sub_dict_greeks[each],width=10,text=str(TrueValue),fg=color)
                lb.pack(fill='x',side='top')
        
        for each in list(self.sec_sub_dict_greeks.keys()):
            color = 'red' if res_total[each]>=0 else 'green'
            lb = Label(self.sec_sub_dict_greeks[each],width=10,text=str(round(res_total[each],3)),fg=color)
            lb.pack(fill='x',side='top')

        
        
    def create_vol_widgets(self):
        vol_buy,vol_sell = self.cal_vol()
        self.QuantVol = []
        
        for i in range(len(vol_buy)):
            tmp = vol_sell[i] if self.info_vol[i][4] else vol_buy[i]  #若买，则计算greeks用vol_buy,反之用vol_sell
            self.QuantVol.append(tmp)
        
        self.clear(self.sec_sub_dict_vol)
        
        for i in range(len(self.QuantVol)):
            for each in list(self.sec_sub_dict_vol.keys()):
                TrueValue = self.QuantVol[i]
                lb = Label(self.sec_sub_dict_vol[each],width=10,text=str(round(TrueValue,3)))
                lb.pack(fill='x',side='top')
                self.vol_lst.append(TrueValue)
                
                

    def cal_greeks(self):
        res = []
        for i in range(len(self.box)):
            if self.info_greeks[i][7][:3] == 'oao':
                CurDay = self.info_greeks[i][1]
                MatDay = self.info_greeks[i][2]
                FixBeg = self.info_greeks[i][3]
                FixEnd = self.info_greeks[i][4]
                z = OptionPricer.random_gen(N=10000,T=500)
                #random,S,SA,r,sigma,K,price_date,maturity_date,start_fixed_date,end_fixed_date,status
                #print(self.box[i]['CurrentPrice'].get())
                #print(type(self.box[i]['CurrentPrice'].get()))
                V = Greeks.Aisan_Greeks(z,float(self.box[i]['CurrentPrice'].get()),float(self.box[i]['HistoricalAvg'].get()),\
                                        self.info_greeks[i][6],self.vol_lst[i],float(self.info_greeks[i][0]),\
                                        CurDay,MatDay,FixBeg,FixEnd,self.info_greeks[i][8])
                res_tmp = V.cpt_all_greeks()
                res.append(res_tmp)
            
            elif self.info_greeks[i][7][:3] == 'ovo':
                CurDay = self.info_greeks[i][1]
                MatDay = self.info_greeks[i][2]
                T = (MatDay-CurDay).days/365
                #S,r,sigma,K,T,status
                V = Greeks.Greeks_Euro(float(self.box[i]['CurrentPrice'].get()),self.info_greeks[i][6],\
                                       self.vol_lst[i],float(self.info_greeks[i][0]),\
                                       T,self.info_greeks[i][8])
                res_tmp = V.cpt_all_greeks()
                res.append(res_tmp)
            
            else:
                pass
        
        return res
        
    def cal_vol(self):
        VB = []
        VS = []
        for i in range(len(self.box)):
            #print(type(self.info_vol[i][2]),type(self.info_vol[i][3][0]))
            vol_buy,vol_sell = Tprice_RealTime.cal_buy_sell_vol(self.info_vol[i][0]+'-'+self.info_vol[i][1],\
                                                   float(self.box[i]['CurrentPrice'].get()),\
                                                   self.info_vol[i][2],self.info_vol[i][3])
            
            VB.append(vol_buy['vol'].values[0])
            VS.append(vol_sell['vol'].values[0])
            
        return VB,VS
   
   



a = Application()
a.create_section()
a.init_widgets()
a.StartQuote()

#a.root.mainloop()






