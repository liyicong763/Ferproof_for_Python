import math
from random import sample
import time
from itertools import combinations

from pandas.tests.extension import decimal

from paint import paint, time_paint


def num(n):
    a, b, c = 0, 0, 0
    temp0, temp1, temp2, temp3 = 0, 0, 0, 0
    temp0 = int(n ** 0.5)
    if temp0 ** 2 == n:
        return [temp0], 1

    a = n - temp0 ** 2
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

    while t != 0:
        if int(((temp0 ** 2 - t ** 2) + c) ** 0.5) ** 2 == (temp0 ** 2 - t ** 2) + c:
            temp3 = int(((temp0 ** 2 - t ** 2) + c) ** 0.5)
            temp0 = t
            return [temp0, temp1, temp2, temp3], 444444
        t = t - 1
    t = temp1 - 1
    while t != 0:
        if int(((temp1 ** 2 - t ** 2) + c) ** 0.5) ** 2 == (temp1 ** 2 - t ** 2) + c:
            temp3 = int(((temp1 ** 2 - t ** 2) + c) ** 0.5)
            temp1 = t
            return [temp0, temp1, temp2, temp3], 444444
        t = t - 1
    t = temp2 - 1
    while t != 0:
        if int(((temp2 ** 2 - t ** 2) + c) ** 0.5) ** 2 == (temp2 ** 2 - t ** 2) + c:
            temp3 = int(((temp2 ** 2 - t ** 2) + c) ** 0.5)
            temp2 = t
            return [temp0, temp1, temp2, temp3], 444444
        t = t - 1
    return [temp0, temp1, b, c], 404


def numSquares(n):
    a, b, c = 0, 0, 0
    temp0, temp1, temp2, temp3 = 0, 0, 0, 0
    temp0 = int(n ** 0.5)
    for i in range(n):
        temp0 = int((n - i) ** 0.5)
        if temp0 ** 2 == n - i:
            if i == 0:
                return [temp0], 1
            else:
                a = i
                break
    for ii in range(a):
        temp1 = int((a - ii) ** 0.5)
        if temp1 ** 2 == a - ii:
            if ii == 0:
                return [temp0, temp1], 2
            else:
                b = ii
                break
    for iii in range(b):
        temp2 = int((b - iii) ** 0.5)
        if temp2 ** 2 == b - iii:
            if iii == 0:
                return [temp0, temp1, temp2, 0], 4
            else:
                c = iii
                break
    for iiii in range(c):
        temp3 = int((c - iiii) ** 0.5)
        if temp3 ** 2 == c - iiii:
            if iiii == 0:
                return [temp0, temp1, temp2, temp3], 4
    t = temp0 ** 2
    for i in range(t):
        if int((t - i) ** 0.5) ** 2 == t - i and int((i + c) ** 0.5) ** 2 == i + c:
            temp0 = int((t - i) ** 0.5)
            temp3 = int((i + c) ** 0.5)
            return [temp0, temp1, temp2, temp3], 444444
    t = temp1 ** 2
    for i in range(t):
        if int((t - i) ** 0.5) ** 2 == t - i and int((i + c) ** 0.5) ** 2 == i + c:
            temp1 = int((t - i) ** 0.5)
            temp3 = int((i + c) ** 0.5)
            return [temp0, temp1, temp2, temp3], 444444
    t = temp2 ** 2
    for i in range(t):
        if int((t - i) ** 0.5) ** 2 == t - i and int((i + c) ** 0.5) ** 2 == i + c:
            temp2 = int((t - i) ** 0.5)
            temp3 = int((i + c) ** 0.5)
            return [temp0, temp1, temp2, temp3], 444444
    return [temp0, temp1, b, c], 404


def xx(n):
    a, b, c = 0, 0, 0
    temp0, temp1, temp2, temp3 = 0, 0, 0, 0
    temp0 = int(math.log(n, 2))
    if 2 ** temp0 == n:
        return [temp0], 1

    a = n - 2 ** temp0
    temp1 = int(math.log(a, 2))
    if 2 ** temp1 == a:
        return [temp0, temp1], 2

    b = a - 2 ** temp1
    temp2 = int(math.log(b, 2))
    if 2 ** temp2 == b:
        return [temp0, temp1, temp2, 0], 4

    c = b - 2 ** temp2
    temp3 = int(math.log(c, 2))
    if 2 ** temp3 == c:
        return [temp0, temp1, temp2, temp3], 4
    return [temp0, temp1, temp2, c], 404


def s(data):
    pfs = [1]

    def gen():
        n = max(data)
        for num in range(2, int(n ** 0.5) + 1):
            for _ in range(4):
                pfs.append(num ** 2)

    gen()

    def getresult(num):
        temp = int(num ** 0.5) ** 2
        index = pfs.index(temp) + 1
        tempfs = pfs[:index]
        for length in range(1, 5):
            for item in combinations(pfs, length):
                if sum(item) == num:
                    return item
        return None

    for num in data:
        print(num, ':', getresult(num))


def Gcd(x, y, z):
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


def floatGcd(x, y, z):
    len_x = len(str(x).split(".")[1])
    len_y = len(str(y).split(".")[1])
    len_z = len(str(z).split(".")[1])
    print(len_x, len_y, len_z)
    if len_x >= len_y and len_x >= len_z:
        return 10 ** len_x
    elif len_y >= len_x and len_y >= len_z:
        return 10 ** len_y
    else:
        return 10 ** len_z


def xxx(a):
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


'''data = sample(range(1, 9999999), 2000)
#s([300000000])
a, b = 0, 0
for i in data:
  x, y = xx(i)
  print(i, x, y)
  if y == 404:
      a += 1
  else:
      b += 1
print(b / (a + b))'''

prove_time1 = []
prove_time2 = []
# [10,50,100,500, 1000,5000,10000,50000,100000,500000,1000000,5000000,10000000,50000000,100000000]
#data = sample(range(1, 999), 20)
for i in [111,1111,11111,111111,1111111,11111111]:
    prove_time_start1 = time.time()
    temp = [i]
    s(temp)
    prove_time_end1 = time.time()
    prove_time1.append((prove_time_end1 - prove_time_start1) * 1000)
    print((prove_time_end1 - prove_time_start1) * 1000)

    prove_time_start2 = time.time()
    x, y, z = xxx(i)
    prove_time_end2 = time.time()
    print((prove_time_end2 - prove_time_start2))
    prove_time2.append((prove_time_end2 - prove_time_start2) * 1000)
# print(floatGcd(3.55 ,4.67 ,8.251876876878))
# s([230000])
time_paint(prove_time1, prove_time2)