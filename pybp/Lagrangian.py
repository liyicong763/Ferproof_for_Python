
def Gcd(x ,y ,z):

    while y != 0:
        temp = y
        y = x % y
        x = temp

    if x < z:
        temp = x
        x = z
        z = temp

    while z != 0:
        temp = z
        z = x % z
        x = temp
    return x

def floatGcd(x ,y ,z):
    len_x = len(str(x).split(".")[1])
    len_y = len(str(y).split(".")[1])
    len_z = len(str(z).split(".")[1])
    if (len_x >= len_y and len_x >= len_z):
        return 10 ** len_x
    elif (len_y >= len_x and len_y >= len_z):
        return 10 ** len_y
    else:
        return 10 ** len_z

def numSquares(n):
    a, b, c = 0, 0, 0
    temp0, temp1, temp2, temp3 = 0, 0, 0, 0
    temp0 = int(n ** 0.5)
    if temp0 ** 2 == n:
        return [temp0], 1
    a = n - (temp0 ** 2)
    temp1 = int(a ** 0.5)
    if temp1 ** 2 == a:
        return [temp0, temp1], 2

    b = a - temp1 ** 2
    temp2 = int(b ** 0.5)
    if temp2 ** 2 == b:
        return [temp0, temp1, temp2, 0], 4

    c = b - temp2 ** 2
    temp3 = int(c ** 0.5)
    if temp3 ** 2 == c:
        return [temp0, temp1, temp2, temp3], 4
    t = temp0 - 1
    return [temp0, temp1, temp2, temp3], 4

def novel_numSquares(a):
    sp_num = {
        23: [1, 2, 3, 3],
        32: [4, 4, 0, 0],
        43: [3, 3, 5, 0],
        48: [4, 4, 4, 0],
        56: [2, 4, 6, 0],
        61: [5, 6, 0, 0],
        71: [1, 3, 5, 6],
        76: [2, 6, 6, 0],
        79: [1, 2, 5, 7],
        88: [4, 6, 6, 0],
        93: [2, 5, 8, 0],
        96: [4, 4, 8, 0]
    }
    temp_list = []
    temp_a = a
    if temp_a in sp_num:
        return sp_num[temp_a], [0, 0, 0, 0], 4
    for i in range(0, 4):
        sqrt_temp_a = int(temp_a ** 0.5)
        temp_list.append(sqrt_temp_a)
        if sqrt_temp_a ** 2 == temp_a:
            if i == 2:
                temp_list.append(0)
                i = 3
            zero = []
            for z in range(i + 1):
                zero.append(0)
            return temp_list, zero, i + 1
        if i == 3:
            temp_a = temp_a - (sqrt_temp_a ** 2)
            print(temp_a)
            if temp_a in sp_num:
                return temp_list, sp_num[temp_a], 4
            else:
                sub_temp_list = []
                sub_temp_a = temp_a
                for ii in range(0, 4):
                    sub_sqrt_temp_a = int(sub_temp_a ** 0.5)
                    sub_temp_list.append(sub_sqrt_temp_a)
                    if sub_sqrt_temp_a ** 2 == sub_temp_a:
                        bu_0 = 4 - len(sub_temp_list)
                        if bu_0 != 0:
                            for bu_0i in range(bu_0):
                                sub_temp_list.append(0)
                        return temp_list, sub_temp_list, 4
                    sub_temp_a = sub_temp_a - (sub_sqrt_temp_a ** 2)
                return None
        temp_a = temp_a - (sqrt_temp_a ** 2)

def int_numSquares(n):
    a, b, c = 0, 0, 0
    temp0, temp1, temp2, temp3 = 0, 0, 0, 0
    temp0 = int(n ** 0.5)
    if temp0 ** 2 == n:
        return [temp0, temp0, temp0, temp0, temp0, temp0, temp0, temp0], 8
    a = n - (temp0 ** 2)
    temp1 = int(a ** 0.5)
    if temp1 ** 2 == a:
        return [temp0, temp1, temp0, temp1, temp0, temp1, temp0, temp1], 8

    b = a - temp1 ** 2
    temp2 = int(b ** 0.5)
    if temp2 ** 2 == b:
        return [temp0, temp1, temp2, 0, temp0, temp1, temp2, 0], 8

    c = b - temp2 ** 2
    temp3 = int(c ** 0.5)
    if temp3 ** 2 == c:
        return [temp0, temp1, temp2, temp3, temp0, temp1, temp2, temp3], 8
    t = temp0 - 1
    return [temp0, temp1, temp2, temp3, temp0, temp1, temp2, temp3], 8
