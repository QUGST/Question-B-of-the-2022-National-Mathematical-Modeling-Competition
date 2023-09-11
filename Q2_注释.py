import math

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


def Q1_solve(name_send_1, name_send_2, name_get_1, angle_send1_get1_FY00, angle_send2_get1_FY00,
             angle_send1_get1_send2):
    r = 1  # 无人机所在的圆的半径
    name_send_1 = int(str(name_send_1).split('FY')[1])  # 处理编号
    name_send_2 = int(str(name_send_2).split('FY')[1])  # 处理编号
    name_get_1 = int(str(name_get_1).split('FY')[1])  # 处理编号
    ct = min([math.fabs(name_send_1 - name_send_2), math.fabs(name_send_2 - name_send_1),
              math.fabs(name_send_2 + 9 - name_send_1), math.fabs(name_send_1 - 9 - name_send_2)])
    ct = ct * math.pi * 4 / 18  # 第一个发信号无人机和FY00和第二个发信号无人机的角的角度
    d = math.sqrt(2 * r * r - 2 * r * r * math.cos(ct))  # 第一个发信号无人机和第二个发信号无人机的距离
    ini = []  # 初始解
    ct = min([math.fabs(name_send_1 - name_get_1), math.fabs(name_get_1 - name_send_1),
              math.fabs(name_send_1 + 9 - name_get_1), math.fabs(name_get_1 - 9 - name_send_1)])
    ct = ct * math.pi * 4 / 18  # 理想情况下第一个发信号无人机和接受信号的无人机和FY00的角的角度
    ini.append(math.sqrt(2 * r * r - 2 * r * r * math.cos(ct)))  # 理想情况下第一个发信号无人机和接受信号无人机的距离
    ini.append(r)  # 理想情况下FY00和接受信号无人机的距离
    ct = min([math.fabs(name_send_2 - name_get_1), math.fabs(name_get_1 - name_send_2),
              math.fabs(name_send_2 + 9 - name_get_1), math.fabs(name_get_1 - 9 - name_send_1)])
    ct = ct * math.pi * 4 / 18  # 理想情况下第一个发信号无人机和接受信号的无人机和FY00的角的角度
    ini.append(math.sqrt(2 * r * r - 2 * r * r * math.cos(ct)))  # 理想情况下第一个发信号无人机和接受信号无人机的距离
    return func(name_send_1, name_send_2, name_get_1, angle_send1_get1_FY00, angle_send2_get1_FY00,
                angle_send1_get1_send2, ini, d, r)  # 计算接受信号的无人机极坐标


def Q2_solve(angle_01, angle_0n, angle_1n, angle_0m, angle_1m, name_get_1):
    table = do_table()  # 计算理想情况下各个无人机之间形成的夹角
    array_n = []  # 穷举第一个未知编号的无人机的的编号后得到的接受信号的无人机的可能的位置
    array_m = []  # 穷举第二个未知编号的无人机的的编号后得到的接受信号的无人机的可能的位置
    self = int(str(name_get_1).split('FY')[1]) - 1  # 处理接受信号的无人机的编号
    for i in range(1, 9):  # 穷举可能的无人机的编号
        name_send_n = 'FY0' + str(i + 1)  # 形成编号
        if (name_send_n == name_get_1 or math.fabs(table[0][i][self][0] - angle_01) > 0.5 or math.fabs(
                table[0][i][self][1] - angle_0n) > 0.5 or math.fabs(table[0][i][self][2] - angle_1n) > 0.5):
            continue
        # 处理偏差过大的情况，或者编号冲突的情况

        array_n.append(
            (i + 1, Q1_solve('FY01', name_send_n, name_get_1, angle_01, angle_0n, angle_1n)))  # 记录计算的接受信号的无人机的可能坐标
    for i in range(1, 9):  # 穷举可能的无人机的编号
        name_send_m = 'FY0' + str(i + 1)  # 形成编号
        if (name_send_m == name_get_1 or math.fabs(table[0][i][self][0] - angle_01) > 0.5 or math.fabs(
                table[0][i][self][1] - angle_0m) > 0.5 or math.fabs(table[0][i][self][2] - angle_1m) > 0.5):
            continue
        # 处理偏差过大的情况，或者编号冲突的情况
        array_m.append(
            (i + 1, Q1_solve('FY01', name_send_m, name_get_1, angle_01, angle_0m, angle_1m)))  # 记录计算的接受信号的无人机的可能坐标

    for i in array_n:  # 遍历可能的坐标点，最接近的两个坐标的就是接受无人机的坐标
        for j in array_m:
            if (math.fabs(i[1][0] - j[1][0]) <= 0.3):
                return_len = (i[1][0] + j[1][0]) / 2

                if (math.fabs(i[1][1] - j[1][1]) <= 10):
                    return_angle = (i[1][1] + j[1][1]) / 2

                    return (i[0], j[0], return_len, return_angle)

                elif (math.fabs(i[1][1] - j[1][1]) >= 350):
                    return_angle = (i[1][1] + j[1][1]) / 2 + 180

                    return (i[0], j[0], return_len, return_angle)

            elif (math.fabs(i[1][0] - j[1][0]) >= 5.8):
                return_len = (i[1][0] + j[1][0]) / 2 + math.pi
                if (math.fabs(i[1][1] - j[1][1]) <= 10):
                    return_angle = (i[1][1] + j[1][1]) / 2

                    return (i[0], j[0], return_len, return_angle)

                elif (math.fabs(i[1][1] - j[1][1]) >= 350):
                    return_angle = (i[1][1] + j[1][1]) / 2 + 180

                    return (i[0], j[0], return_len, return_angle)  # 返回两家未知编号的无人机的编号和接收信号的无人机的位置


if __name__ == "__main__":
    angle_FY01_get1_FY00 = 0.584  # 第一个FY01与接受信号的无人机和FY00形成的角度
    angle_send1_get1_FY00 = 0.132  # 第一个未知位置的发信号无人机与接受信号的无人机和FY00形成的角度
    angle_send1_get1_FY01 = 0.716  # 第一个未知位置的发信号无人机与接受信号的无人机和FY01形成的角度
    angle_send2_get1_FY00 = 0.852  # 第二个未知位置的发信号无人机与接受信号的无人机和FY00形成的角度
    angle_send2_get1_FY01 = 1.436  # 第二个未知位置的发信号无人机与接受信号的无人机和Fy01形成的角度
    name_get = 'FY04'  # 接受信号的无人机编号
    print(Q2_solve(angle_FY01_get1_FY00, angle_send1_get1_FY00, angle_send1_get1_FY01, angle_send2_get1_FY00,
                   angle_send2_get1_FY01, name_get))  # 计算两家未知编号的无人机的编号和接收信号的无人机的位置
