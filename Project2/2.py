import random
from SM3 import sm3_hash
from gmssl import sm3

def rho_method():
    hashlist = []
    x = random.randint(0, 2**32) #原像长为32bit，
    print('初始x:',x)
    x_1 = sm3_hash(bin(x)[2:]).replace(" ","")
    hashlist.append(x_1)
    while(True):
        bin_str = ""
        for n in hashlist[-1]:
            bin_str += bin(int(n, 16))[2:].zfill(4)
        x_2 = sm3_hash(bin_str).replace(" ","")
        for i in hashlist:
            if x_2[0:4]==i[0:4]:
                return i,hashlist.index(hashlist[-1]),hashlist.index(i)
            else:
                hashlist.append(x_2)
                break

m,x1,x2=rho_method()
print('发生碰撞，碰撞的哈希值为：', m)
print('对应的原像序号分别为：：', x1, x2)
