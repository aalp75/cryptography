from prime_number import *

def complete_with_0(list_input, size):
    res = []
    for elmt in list_input:
        tmp = elmt
        for _ in range(len(tmp), size):
            tmp = "0" + tmp
        res.append(tmp)
    return res


def bloc_s1_to_s2(list_s1, s1, s2):
    new_list = []
    index = 0
    tmp = ""
    for elmt in reversed(list_s1):
        for i in range(s1):
            tmp = elmt[s1 - 1 - i] + tmp
            index += 1
            if len(tmp) == s2:
                new_list.insert(0, tmp)
                index = 0
                tmp = ""
    if len(tmp) > 0 and len(tmp) < s2:
        cond = False
        for i in range(len(tmp)):
            if tmp[i] != "0":
                cond = True
                break
        if cond:
            for _ in range(len(tmp), s2):
                tmp = "0" + tmp
            new_list.insert(0, tmp)
    return new_list


def list_to_string(s):
    str1 = ""
    for ele in s:
        str1 += ele
    return str1


def extended_euclidean(a, b):
    r, u, v, r2, u2, v2 = a, 1, 0, b, 0, 1
    r = a * u + b * v
    r2 = a * u2 + b * v2
    while r2 != 0:
        q = r // r2
        r, u, v, r2, u2, v2 = r2, u2, v2, r - q * r2, u - q * u2, v - q * v2
        r = a * u + b * v
        r2 = a * u2 + b * v2
    if v < 0:
        v = v + a
        u = -u - 1
    return r, u, v


def find_key(p, q):
    phi = (p - 1) * (q - 1)
    for i in range(max(p, q) + 1, phi):
        if pgcd(i, phi) == 1:
            return i
    return 0
