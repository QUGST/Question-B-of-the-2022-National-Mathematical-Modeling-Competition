# _*_ coding: UTF-8 _*_
# @Time : 2022/9/15 21:43
# @Dile : Q1_注释.py
# writer :yangquan
import math

import numpy as np
import sympy as sp
c1 = math.pi / 7;#角度1
c2 = math.pi / 6;#角度2
d = 0
r = 1#半径
ini=[]

def func(a,b,c):
    #print('x')
    x = sp.Symbol('x')
    y = sp.Symbol('y')
    z = sp.Symbol('z')
    global c1, c2, d
    solved_value = sp.nsolve([
        (x ** 2 + z ** 2 - d ** 2) / (2 * x * z) - sp.cos(c1 + c2),
        (x ** 2 + y ** 2 - r ** 2) / (2 * x * y) - sp.cos(c1),
        (y ** 2 + z ** 2 - r ** 2) / (2 * y * z) - sp.cos(c2)
    ],[x,y,z], ini)
    x=solved_value[0]
    y=solved_value[1]
    z=solved_value[2]

    print((x ** 2 + y ** 2 - r ** 2) / (2 * x * y) - sp.cos(c1))
    print((z ** 2 + y ** 2 - r ** 2) / (2 * z * y) - sp.cos(c2))


def fift(a,b,c):
    a=int(str(a).split('FY')[1])
    b = int(str(b).split('FY')[1])
    c = int(str(c).split('FY')[1])
    ct=min([math.fabs(a-b),math.fabs(b-a),math.fabs(a+9-b),math.fabs(b+9-a)])
    ct=ct*math.pi*4/18
    global d,r,ini
    d=math.sqrt(2*r*r-2*r*r*math.cos(ct))
    ini=[]
    ct = min([math.fabs(a - c), math.fabs(c - a), math.fabs(a + 9 - c), math.fabs(c + 9 - a)])
    ct = ct * math.pi * 4 / 18
    ini.append(math.sqrt(2*r*r-2*r*r*math.cos(ct)))
    ini.append(r)
    ct = min([math.fabs(b - c), math.fabs(c - b), math.fabs(b + 9 - c), math.fabs(c + 9 - b)])
    ct = ct * math.pi * 4 / 18
    ini.append(math.sqrt(2 * r * r - 2 * r * r * math.cos(ct)))


if __name__ =='__main__':
    fift('FY01','FY04','FY07')#飞机编号

    func('FY01','FY04','FY07')