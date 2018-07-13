# -*- coding: utf-8 -*-
"""
Created on Wed May 16 09:42:16 2018

@author: Harrison
"""

import GetDataMySQL
import TimeSeriesInterpolator
import pandas as pd 
import numpy as np
from scipy.stats import norm

def BAspread(df,param_list):
    para = param_list
    buy_sell_para = df.copy()
    for each in para:
        buy_sell_para[each] = df[each+'_offset']
        
    return buy_sell_para

def cal_buy_sell_vol(future,f_atm,Tdays,strike_lst):
    in_put = {'TimeToMaturity':Tdays,'strike':strike_lst}
    
    myfuture = future
    param_list = ['vol_ref', 'vcr', 'slope_ref', 'scr','dn_cf', 'up_cf',\
                  'put_curv', 'call_curv','dn_sm', 'up_sm', 'dn_slope', 'up_slope']
    
    benchmark =  GetDataMySQL.get_std_paramdata(myfuture.split('-')[0],myfuture.split('-')[1],model='wing')
    benchmark['f_atm'] = f_atm
    benchmark_bs = BAspread(benchmark,param_list)
    
    benchmark = benchmark[['alpha','f_atm','f_ref','ssr','vol_ref','vcr',\
                             'slope_ref','scr','dn_cf','up_cf','call_curv',\
                             'dn_sm','up_sm','dn_slope','up_slope','put_curv','day']]
    
    benchmark_bs = benchmark_bs[['alpha','f_atm','f_ref','ssr','vol_ref','vcr',\
                             'slope_ref','scr','dn_cf','up_cf','call_curv',\
                             'dn_sm','up_sm','dn_slope','up_slope','put_curv','day']]
    
    benchmark.index = [0]*len(benchmark)
    benchmark_bs.index = [0]*len(benchmark_bs)
    
    vol_mid = TimeSeriesInterpolator.time_interpolate(benchmark,in_put)
    vol_bs = TimeSeriesInterpolator.time_interpolate(benchmark_bs,in_put)
    
    vol_mid.set_index('strike',inplace=True)
    vol_bs.set_index('strike',inplace=True)
    
    vol_buy = vol_mid-vol_bs
    vol_sell = vol_mid+vol_bs
    
    vol_buy.reset_index(inplace=True)
    vol_sell.reset_index(inplace=True)
    
    return vol_buy,vol_sell

def Tprice_realtime(strikeprice,step,increment,temp_input):
    '''ATM strikeprice'''
    '''上下实虚档数'''
    '''档数步幅'''
   
    S=temp_input[0]
    T=temp_input[1]
    r=temp_input[2]
    q=temp_input[3]
    myfuture = temp_input[4]
    
    kk=[]
    vol = []
#%% 判断每步间隔大小
    if strikeprice*increment>2.5:
        incrementamount=round(increment*strikeprice/5)*5
    else:
        incrementamount=round(increment*strikeprice)    
#%% 产生strike序列
    Kprice_lst = [incrementamount*i+strikeprice for i in range(-step,step+1)]
    vol_buy,vol_sell = cal_buy_sell_vol(myfuture,S,T*365,Kprice_lst)
#%% 循环输出T形状列表 
    for i in range(-step,step+1):
        
        Kprice = incrementamount*i+strikeprice
        sigma_buy = vol_buy[vol_buy['strike']==Kprice]['vol'].values[0]
        
        sigma_sell = vol_sell[vol_sell['strike']==Kprice]['vol'].values[0]
        
        ecb=round(European_Call(S,Kprice,T,sigma_buy,r,q),4)
        epb=round(European_Put(S,Kprice,T,sigma_buy,r,q),4)
        ecs=round(European_Call(S,Kprice,T,sigma_sell,r,q),4)
        eps=round(European_Put(S,Kprice,T,sigma_sell,r,q),4)
        
        K=[epb,eps,Kprice,ecb,ecs]
        vol_row = [sigma_buy,sigma_sell,Kprice,sigma_buy,sigma_sell]
        
        kk.append(K)
        vol.append(vol_row)
    
    kk=pd.DataFrame(kk,columns=['看跌买价','看跌卖价','执行价','看涨买价','看涨卖价'])
    vol = pd.DataFrame(vol,columns=['看跌买方波动率','看跌卖方波动率','执行价','看涨买方波动率','看涨卖方波动率'])
    
    kk = kk.sort_values(by='执行价',axis=0,ascending=False)
    vol = vol.sort_values(by='执行价',axis=0,ascending=False)
    
    kk.reset_index(inplace=True,drop=True)
    vol.reset_index(inplace=True,drop=True)
    
    return kk,vol

#%% 欧式看涨期权定价
def European_Call(S,K,T,sigma,r,q):
    
    d1 = (np.log(S/K)+(r-q+0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    d2 = (np.log(S/K)+(r-q-0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    V = S*np.exp(-q*T)*norm.cdf(d1)-K*np.exp(-r*T)*norm.cdf(d2)

    return V
#%% 欧式看跌期权定价
def European_Put(S,K,T,sigma,r,q):

    d1 = (np.log(S/K)+(r-q+0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    d2 = (np.log(S/K)+(r-q-0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    V =K*np.exp(-r*T)*norm.cdf(-d2)-S*np.exp(-q*T)*norm.cdf(-d1)

    return V


if __name__ == '__main__':  
    myfuture_lst = GetDataMySQL.get_future_info()
    myfuture = myfuture_lst[1]
    strikeprice = 2800
    step = 5
    increment = 0.01
    f_atm = 2850
    Tdays = 90
    #vol_buy,vol_sell = cal_buy_sell_vol(myfuture,f_atm,Tdays,strike_lst)
    #print(vol_buy)
    #print(vol_sell)
    temp_input = [f_atm,Tdays/365,0.01,0,myfuture]
    out_put1,out_put2 = Tprice_realtime(strikeprice,step,increment,temp_input)
    print(out_put1)
    print(out_put2)
    
    
    