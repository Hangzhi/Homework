# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 08:51:45 2018

@author: Lenovo
"""



                
        
#print(123)
bdg=[]
rev=0
mom=0
for j in range(12):
    a=input()
    bdg.append(a)
for i in range(12):
    if((rev+300-int(bdg[i])<0):
        print(0)
        print ('-',i+1)
        break
    else:
        print(0)
        rev=rev+300-int(bdg[i])
        print(rev,bdg[i],mom)
        if(rev//100>0):
            mom+=(rev//100)*100
        rev=rev%100
mom=mom*1.2
print(mom)