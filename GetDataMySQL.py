# -*- coding: utf-8 -*-
"""
Created on Fri May 25 10:54:50 2018

@author: Harrison
"""
import pymysqlread
import pandas as pd

def getparamdata(exchange,index,model='wing'):        #获取exchange-index的参数数据
    #%% 获取数据库数据
    modelinstance=exchange+'-'+index
    strall='SELECT * FROM futurexdb.model_params where accountid=20 and model= '+"'wing' " +'and modelinstance like'+"'%"+modelinstance+"%'"
    data=pymysqlread.dbconn(strall)                             #读取函数pymysqlread
    #%%整理数据表
    days = data.modelinstance.drop_duplicates().tolist()
    Totaltable=[]
    bench_day = []
    for i in range(len(days)):
        b=data[data['modelinstance']==days[i]]                  #按时间分割
        b.reset_index(inplace=True,drop=True)                   #重置index
        bb=b.pivot('modelinstance','paramname','paramvalue')    #转换数据表头
        bb['day']=int(days[i].split('-')[2])                    #加入日期列
        bench_day.append(int(days[i].split('-')[2]))
        Totaltable.append({'days':days[i],'data':bb})
    return Totaltable,bench_day
#%%获取所有合约信息
def get_future_info():
    mysql = 'select Distinct modelinstance from futurexdb.model_params where accountid = 20'
    data = pymysqlread.dbconn(mysql)
    data['modelinstance'] = data['modelinstance'].apply(lambda x:x.split('-')[0]+'-'+x.split('-')[1])
    data = data.drop_duplicates()['modelinstance'].tolist()
    return data
#%%标准化dataframe
def get_std_paramdata(exchange,index,model='wing'):
    data,bench_day = getparamdata(exchange,index,model='wing')
    res = pd.DataFrame()
    for each in data:
        res = pd.concat([res,each['data']], axis=0, join_axes=[each['data'].columns])
    return res

#%%使用方法
if __name__ == '__main__':
    a,b=getparamdata(exchange='DCE',index='C',model='wing')
    alpha=list(a[0]['data'].alpha)                              #获取第一个表的alpha值
    day=list(a[0]['data'].day)                                  #获取第一个表的day值
    print(alpha,day)
    res = get_std_paramdata(exchange='DCE',index='C',model='wing')