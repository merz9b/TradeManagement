# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 10:59:49 2018

@author: Jax_GuoSen
"""

class A:
    def __init__(self,x):
        self.x = x
class B(A):
    #def __init__(self,y):
    #    self.y = y
    
    def _print(self):
        print('hello')
        
class C(B):
    def add(self):
        print(self.x)