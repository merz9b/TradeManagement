# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 09:53:49 2018

@author: Jax_GuoSen
"""

import tkinter
from  tkinter import ttk  #导入内部包
'''
class MainForm:
    def __init__(self):
        self.root=Tk()
        self.frame=self.studentsFrame()
        self.w=720
        self.h=400
        self.frame.pack()
        self.root.mainloop()
#4@books prepares
    def booksFrame(self):
        frame=Frame(self.root,width=self.w,height=self.h)
        #frame.grid(row=0,column=0,sticky=W)        
        #frame.pack(padx=0,pady=0)
        #Label(frame, text = '所有学生').pack(side=TOP)
        tree = ttk.Treeview(frame,height=18, columns=('a','b','c','d','e','f'))
        tree.column('a', width=140, anchor='center')
        tree.column('b', width=60, anchor='center')
        tree.column('c', width=80, anchor='center')
        tree.column('d', width=80, anchor='center')
        tree.column('e', width=80, anchor='center')
        tree.column('f', width=40, anchor='center')
        tree.heading('a', text='书名')
        tree.heading('b', text='作者')
        tree.heading('c', text='出版时间')
        tree.heading('d', text='出版社')
        tree.heading('e', text='类型')
        tree.heading('f', text='库存')        
        vbar = ttk.Scrollbar(frame,orient=VERTICAL,command=tree.yview)
        tree.configure(yscrollcommand=vbar.set)
        #tree.pack()
        #vbar.pack()        
        tree.grid(row=0,column=0,sticky=NSEW)
        vbar.grid(row=0,column=1,sticky=NS)
        items=getBooks()
        i=0
        for item in items:
            tree.insert('',i,values=("《"+item[1]+"》",item[2],item[3],item[4],item[5],item[6]))
            i=i+1
        return frame
    
a = MainForm()

'''

win=tkinter.Tk()
tree=ttk.Treeview(win)#表格
tree["columns"]=("姓名","年龄","身高")
tree.column("姓名",width=100)   #表示列,不显示
tree.column("年龄",width=100)
tree.column("身高",width=100)
 
tree.heading("姓名",text="姓名-name")  #显示表头
tree.heading("年龄",text="年龄-age")
tree.heading("身高",text="身高-tall")
 
tree.insert("",0,text="line1" ,values=("1","2","3")) #插入数据，
tree.insert("",1,text="line1" ,values=("1","2","3"))
tree.insert("",2,text="line1" ,values=("1","2","3"))
tree.insert("",3,text="line1" ,values=("1","2","3"))
 
tree.pack()
win.mainloop()
