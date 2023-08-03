from SM3 import sm3_hash
import random

def padding(str):
    n = len(str)
    k = 0
    while((n + 1 + k) % 512 != 448):
        k += 1
        str += '0'
    llen = bin(n)[2:]
    llength = len(llen)
    for i in range(64 - llength+1):
        llen = '0' + llen
    str = str + llen
    return str

M1 = 243276859
M2 = 1418058957
M1_padding = hex(int(padding(bin(M1)[2:]), 2))
M2_padding = hex(int(padding(bin(M2)[2:]), 2))
# H1 = sm3_hash(M1_padding)
# print('H1:',H1)
# M3 = M1_padding + M2_padding[2:]
# H3 = sm3_hash(M3)
# print('H3:',H3)
H2 = sm3_hash(M2_padding)
print('H2:',H2)

