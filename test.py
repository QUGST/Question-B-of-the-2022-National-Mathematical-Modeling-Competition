# _*_ coding: UTF-8 _*_
# @Time : 2022/9/17 13:01
# @Dile : Q3-注释.py
# writer :yangquan
import math

import pandas as pd
import sympy as sp
import numpy as np

if __name__=='__main__':
    data=np.array(pd.read_excel('Q3_迭代.xlsx'))
    out=[]
    for i in data:
        a=[]
        print(i)
        for j in range(10):

           a.append(i[j][0])
           a.append(i[j][1])
        out.append(a)
    print(out)
