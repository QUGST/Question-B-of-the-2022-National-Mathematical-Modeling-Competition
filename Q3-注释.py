# _*_ coding: UTF-8 _*_
# @Time : 2022/9/17 13:01
# @Dile : Q3-注释.py
# writer :yangquan
import cmath
import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sympy as sp


def do_table():  # 返回理想情况下的角度表格
    a = []  # 理想情况下的坐标
    for i in range(9):
        a.append([math.cos(math.pi * i * 4 / 18), math.sin(math.pi * i * 4 / 18)])  # 添加理想点坐标
    table = []
    for i in range(9):  # 穷举第一台发送信号的无人机的编号
        send1 = []
        for j in range(9):  # 穷举第二台发送信号的无人机的编号
            send2 = []
            for k in range(9):  # 穷举接受信号的无人机的编号
                if (i == k or k == j or i == j):  # 处理编号重复的情况
                    send2.append([0, 0, 0])
                    continue
                send3 = []
                send3.append(math.acos(math.sqrt(
                    (a[i][0] - a[k][0]) * (a[i][0] - a[k][0]) + (a[i][1] - a[k][1]) * (a[i][1] - a[k][1])) / 2))
                # 计算第一个发信号无人机与接受信号的无人机和FY00形成的角度
                send3.append(math.acos(math.sqrt((a[j][0] - a[k][0]) * (a[j][0] - a[k][0]) + (
                        a[j][1] - a[k][1]) * (a[j][1] - a[k][1])) / 2))
                # 计算第二个发信号无人机与接受信号的无人机和FY00形成的角度
                send3.append(math.acos((math.pow(a[i][0] - a[k][0], 2) + math.pow(a[i][1] - a[k][1], 2) + math.pow(
                    a[j][0] - a[k][0], 2) + math.pow(a[j][1] - a[k][1], 2) - math.pow(a[i][0] - a[j][0], 2) - math.pow(
                    a[i][1] - a[j][1], 2)) / (2 * math.sqrt(
                    math.pow(a[i][0] - a[k][0], 2) + math.pow(a[i][1] - a[k][1], 2)) * math.sqrt(
                    math.pow(a[j][0] - a[k][0], 2) + math.pow(a[j][1] - a[k][1], 2)))))
                # 计算第一个发信号无人机与接受信号的无人机和第二个发信号无人机形成的角度
                send2.append(send3)
            send1.append(send2)
        table.append(send1)
    return table


def answer(name_send_1, name_send_2, name_get_1, angle_1, angle_2, angle_3, ini, d, r):
    x = sp.Symbol('x')# 设置符号x
    y = sp.Symbol('y')# 设置符号y
    z = sp.Symbol('z')# 设置符号z
    solved_value = sp.nsolve([
        (x ** 2 + z ** 2 - d ** 2) - math.cos(angle_3) * (2 * x * z),
        (x ** 2 + y ** 2 - r ** 2) - math.cos(angle_1) * (2 * x * y),
        (y ** 2 + z ** 2 - r ** 2) - math.cos(angle_2) * (2 * y * z)
    ], [x, y, z], ini, prec=10)# 求解

    x = solved_value[0]# 第一个发信号无人机和接受信号无人机的距离
    y = solved_value[1]# FY00和接受信号无人机的距离
    z = solved_value[2]# 第二个发信号无人机和接受信号无人机的距离

    change = math.acos((y ** 2 + r ** 2 - x ** 2) / (2 * y * r))# 计算第一个发信号无人机和FY00和接受信号无人机的夹角角度
    a = (name_send_1 - 1) * math.pi * 4 / 18# 计算第一个发信号无人机的极角
    a_change = [(a + change + 2 * math.pi) % (2 * math.pi), (a - change + 2 * math.pi) % (2 * math.pi)]# 计算相对于第一个发信号无人机的接受信号无人机的可能位置
    change = math.acos((y ** 2 + r ** 2 - z ** 2) / (2 * y * r))# 计算第二个发信号无人机和FY00和接受信号无人机的夹角角度
    b = (name_send_2 - 1) * math.pi * 4 / 18# 计算第二个发信号无人机的极角
    b_change = [(b + change + 2 * math.pi) % (2 * math.pi), (b - change + 2 * math.pi) % (2 * math.pi)] # 计算相对于第二个发信号无人机的接受信号无人机的可能位置
    ans = 0
    for i in a_change:# 从可能无人机角度中寻找相同的角度，这个角度就是接受信号的无人机的真实极角
        for j in b_change:
            if (math.fabs(i - j) < 0.6):
                ans = (i + j) / 2
            elif (math.fabs(i - j) > 5.7):
                ans = (i + j + 2 * math.pi) / 2

    return (y * math.cos(ans), y * math.sin(ans))# 返回接受信号的无人机的极坐标


def Q1_solve(name_send_1, name_send_2, name_get_1, angle_1, angle_2, angle_3):
    r = 100  # 无人机所在的圆的半径
    name_send_1 = int(str(name_send_1).split('FY')[1])  # 处理编号
    name_send_2 = int(str(name_send_2).split('FY')[1])  # 处理编号
    name_get_1 = int(str(name_get_1).split('FY')[1])  # 处理编号

    ct = min([math.fabs(name_send_1 - name_send_2), math.fabs(name_send_2 - name_send_1),
              math.fabs(name_send_2 - 9 - name_send_1), math.fabs(name_send_1 + 9 - name_send_2)])

    ct = ct * math.pi * 4 / 18  # 第一个发信号无人机和FY00和第二个发信号无人机的角的角度

    d = math.sqrt(2 * r * r - 2 * r * r * math.cos(ct))  # 第一个发信号无人机和第二个发信号无人机的距离
    ini = []  # 初始解
    ct = min([math.fabs(name_send_1 - name_get_1), math.fabs(name_get_1 - name_send_1),
              math.fabs(name_send_1 - 9 - name_get_1), math.fabs(name_get_1 + 9 - name_send_1)])

    ct = ct * math.pi * 4 / 18  # 理想情况下第一个发信号无人机和接受信号的无人机和FY00的角的角度
    ini.append(math.sqrt(2 * r * r - 2 * r * r * math.cos(ct)))
    ini.append(r)
    ct = min([math.fabs(name_send_2 - name_get_1), math.fabs(name_get_1 - name_send_2),
              math.fabs(name_send_2 - 9 - name_get_1), math.fabs(name_get_1 + 9 - name_send_1)])
    # print(ct)
    ct = ct * math.pi * 4 / 18  # 理想情况下第一个发信号无人机和接受信号的无人机和FY00的角的角度

    ini.append(math.sqrt(2 * r * r - 2 * r * r * math.cos(ct)))  # 理想情况下第一个发信号无人机和接受信号无人机的距离

    return answer(name_send_1, name_send_2, name_get_1, angle_1, angle_2, angle_3, ini, d, r)  # 计算接受信号的无人机极坐标


def Q3_solve(Polar):
    r = 100  # 无人机所在的圆的半径
    table = do_table()  # 计算理想情况下各个无人机之间形成的夹角
    Polar = Polar[1:]
    Ideal_location = [(0, 0)]  # 理想情况下点的直角坐标系坐标
    for i in range(1, 10):
        Ideal_location.append((r * math.cos(math.pi * (i - 1) * 40 / 180),
                               r * math.sin(math.pi * (i - 1) * 40 / 180)))  # 计算理想情况下点的直角坐标系坐标
    Right_Angle = np.zeros((10, 2)).tolist()  # 将实际无人机位置的极坐标系坐标转换为直角坐标坐标
    for i in range(1, 10):
        Right_Angle[i][0] = Polar[i - 1][0] * math.cos(Polar[i - 1][1] / 180 * math.pi)
        Right_Angle[i][1] = Polar[i - 1][0] * math.sin(Polar[i - 1][1] / 180 * math.pi)
        # 将实际无人机位置的极坐标系坐标转换为直角坐标坐标
    get_1 = 0  # 记录接受的无人机编号
    ans = []
    for _ in range(500):  # 循环固定次数

        i = (get_1 + 4) % 9 + 1  # 第一台发送信号的无人机的编号
        j = (get_1 + 5) % 9 + 1  # 第二台发送信号的无人机的编号
        k = get_1 + 1  # 接收信号无人机的编号
        get_1 = (get_1 + 1) % 9  # 更新接受信号的无人机编号

        angle_ik = math.acos((math.pow(Right_Angle[i][0] - Right_Angle[k][0], 2) + math.pow(
            Right_Angle[i][1] - Right_Angle[k][1], 2) + math.pow(
            Right_Angle[k][0], 2) + math.pow(Right_Angle[k][1], 2) - math.pow(Right_Angle[i][0], 2) - math.pow(
            Right_Angle[i][1], 2)) / (2 * math.sqrt(
            math.pow(Right_Angle[i][0] - Right_Angle[k][0], 2) + math.pow(Right_Angle[i][1] - Right_Angle[k][1],
                                                                          2)) * math.sqrt(
            math.pow(Right_Angle[k][0], 2) + math.pow(Right_Angle[k][1], 2))))
        angle_ik = (angle_ik + table[i - 1][j - 1][k - 1][0]) / 2  # 第一台发信号无人机与接受信号无人机与FY00间的角度

        angle_jk = math.acos((math.pow(Right_Angle[j][0] - Right_Angle[k][0], 2) + math.pow(
            Right_Angle[j][1] - Right_Angle[k][1], 2) + math.pow(
            Right_Angle[k][0], 2) + math.pow(Right_Angle[k][1], 2) - math.pow(Right_Angle[j][0], 2) - math.pow(
            Right_Angle[j][1], 2)) / (2 * math.sqrt(
            math.pow(Right_Angle[j][0] - Right_Angle[k][0], 2) + math.pow(Right_Angle[j][1] - Right_Angle[k][1],
                                                                          2)) * math.sqrt(
            math.pow(Right_Angle[k][0], 2) + math.pow(Right_Angle[k][1], 2))))
        angle_jk = (angle_jk + table[i - 1][j - 1][k - 1][1]) / 2  # 第二台发信号无人机与接受信号无人机与FY00间的角度

        angle_ij = math.acos((math.pow(Right_Angle[i][0] - Right_Angle[k][0], 2) + math.pow(
            Right_Angle[i][1] - Right_Angle[k][1], 2) + math.pow(
            Right_Angle[j][0] - Right_Angle[k][0], 2) + math.pow(Right_Angle[j][1] - Right_Angle[k][1], 2) - math.pow(
            Right_Angle[i][0] - Right_Angle[j][0], 2) - math.pow(
            Right_Angle[i][1] - Right_Angle[j][1], 2)) / (2 * math.sqrt(
            math.pow(Right_Angle[i][0] - Right_Angle[k][0], 2) + math.pow(
                Right_Angle[i][1] - Right_Angle[k][1], 2)) * math.sqrt(
            math.pow(Right_Angle[j][0] - Right_Angle[k][0], 2) + math.pow(Right_Angle[j][1] - Right_Angle[k][1], 2))))
        angle_ij = (angle_ij + table[i - 1][j - 1][k - 1][2]) / 2  # 第一台发信号无人机与接受信号无人机与第二台发信号无人机间的角度

        A = Q1_solve('FY0' + str(i), 'FY0' + str(j), 'FY0' + str(k), angle_ik, angle_jk, angle_ij)  # 解出接受信号的无人机坐标
        Right_Angle[k][0] += Ideal_location[k][0] - A[0]
        Right_Angle[k][1] += Ideal_location[k][1] - A[1]
        # 进行坐标变换
        jzb = []
        for i in Right_Angle:
            jzb.append(cmath.polar(complex(i[0], i[1])))
        for i in range(10):
            jzb[i] = [list(jzb[i])[0], list(jzb[i])[1] * 180 / math.pi]
        ans.append(jzb)
        # 记录极坐标

    for i in ans:
        for j in range(6, 10):
            i[j][1] += 360
            # 将负角度变为正角度
    pd.DataFrame(ans).to_excel('Q3_迭代.xlsx')
    ans = ans[:][1:]
    ans1 = []  # 记录坐标极径长度
    for i in ans:
        a = []
        for j in range(1, 10):
            a.append(i[j][0])
        ans1.append(a)
    plt.plot(np.std(np.array(ans1), axis=1), 'r')  # 画极径长度的标准差
    ans2 = []
    for i in ans:
        a = []
        for j in range(1, 10):
            a.append(math.fabs(i[j][1] - (j - 1) * 40))

        ans2.append(a)

    plt.plot(np.std(np.array(ans2), axis=1), 'b')  # 画和理想极角的差值的标准差
    plt.legend(['极径长度的标准差', '实际坐标极角和理想极角的差值的标准差'])
    plt.title('迭代次数与精度的变化图')
    plt.show()


def init():
    Polar = [(0, 0), (100, 0), (98, 40.10), (112, 80.21), (105, 119.75), (98, 159.86), (112, 199.96), (105, 240.07),
             (98, 280.17), (112, 320.28)]  # 初始化数据
    return Q3_solve(Polar)


if __name__ == "__main__":
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    init()
