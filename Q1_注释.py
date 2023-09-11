# _*_ coding: UTF-8 _*_
# @Time : 2022/9/15 21:43
# @Dile : Q1_注释.py
# writer :yangquan
import math

import sympy as sp


def func(name_send_1, name_send_2, name_get_1, angle_send1_get1_FY00, angle_send2_get1_FY00, angle_send1_get1_send2,
         ini, d, r):
    x = sp.Symbol('x')  # 设置符号x
    y = sp.Symbol('y')  # 设置符号y
    z = sp.Symbol('z')  # 设置符号z
    solved_value = sp.nsolve([
        (x ** 2 + z ** 2 - d ** 2) / (2 * x * z) - sp.cos(angle_send1_get1_send2),
        (x ** 2 + y ** 2 - r ** 2) / (2 * x * y) - sp.cos(angle_send1_get1_FY00),
        (y ** 2 + z ** 2 - r ** 2) / (2 * y * z) - sp.cos(angle_send2_get1_FY00)
    ], [x, y, z], ini)  # 求解
    x = solved_value[0]  # 第一个发信号无人机和接受信号无人机的距离
    y = solved_value[1]  # FY00和接受信号无人机的距离
    z = solved_value[2]  # 第二个发信号无人机和接受信号无人机的距离

    change = math.acos((y ** 2 + r ** 2 - x ** 2) / (2 * y * r))  # 计算第一个发信号无人机和FY00和接受信号无人机的夹角角度
    angle_send1 = (name_send_1 - 1) * math.pi * 4 / 18  # 计算第一个发信号无人机的极角
    angle_send1_change = [(angle_send1 + change + 2 * math.pi) % (2 * math.pi),
                          (angle_send1 - change + 2 * math.pi) % (2 * math.pi)]  # 计算相对于第一个发信号无人机的接受信号无人机的可能位置

    change = math.acos((y ** 2 + r ** 2 - z ** 2) / (2 * y * r))  # 计算第二个发信号无人机和FY00和接受信号无人机的夹角角度
    angle_send2 = (name_send_2 - 1) * math.pi * 4 / 18  # 计算第二个发信号无人机的极角

    angle_send2_change = [(angle_send2 + change + 2 * math.pi) % (2 * math.pi),
                          (angle_send2 - change + 2 * math.pi) % (2 * math.pi)]  # 计算相对于第二个发信号无人机的接受信号无人机的可能位置

    ans = 0
    for i in angle_send1_change:  # 从可能无人机角度中寻找相同的角度，这个角度就是接受信号的无人机的真实极角
        for j in angle_send2_change:
            if (math.fabs(i - j) < 0.5):
                ans = (i + j) / 2
            elif (math.fabs(i - j) > 6):
                ans = (i + j + 2 * math.pi) / 2

    return (y, ans / math.pi * 180)  # 返回接受信号的无人机的极坐标


def fift(name_send_1, name_send_2, name_get_1, angle_send1_get1_FY00, angle_send2_get1_FY00, angle_send1_get1_send2):
    r = 1  # 无人机所在的圆的半径
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
    ini.append(math.sqrt(2 * r * r - 2 * r * r * math.cos(ct)))  # 理想情况下第一个发信号无人机和接受信号无人机的距离
    ini.append(r)  # 理想情况下FY00和接受信号无人机的距离
    ct = min([math.fabs(name_send_2 - name_get_1), math.fabs(name_get_1 - name_send_2),
              math.fabs(name_send_2 - 9 - name_get_1), math.fabs(name_get_1 + 9 - name_send_1)])
    ct = ct * math.pi * 4 / 18  # 理想情况下第一个发信号无人机和接受信号的无人机和FY00的角的角度
    ini.append(math.sqrt(2 * r * r - 2 * r * r * math.cos(ct)))  # 理想情况下第一个发信号无人机和接受信号无人机的距离
    return func(name_send_1, name_send_2, name_get_1, angle_send1_get1_FY00, angle_send2_get1_FY00,
                angle_send1_get1_send2, ini, d, r)  # 计算接受信号的无人机极坐标


if __name__ == '__main__':
    name_send1 = 'FY09'  # 第一个发信号无人机的编号
    name_send2 = 'FY06'  # 第二个发信号无人机的编号
    name_get1 = 'FY03'  # 接受信号的无人机的编号
    angle_send1_get1_FY00 = 0.524  # 第一个发信号无人机与接受信号的无人机和FY00形成的角度
    angle_send2_get1_FY00 = 0.424  # 第二个发信号无人机与接受信号的无人机和FY00形成的角度
    angle_send1_get1_send2 = 1.047  # 第一个发信号无人机与接受信号的无人机和第二个发信号无人机形成的角度
    print(fift(name_send1, name_send2, name_get1, angle_send1_get1_FY00, angle_send2_get1_FY00,
               angle_send1_get1_send2))  # 输出接受信号的无人机极坐标
