from gmssl import sm3
import string
import time
import random

# 求逆
def exgcd(a, b):
    x1_1, x1_2, x1_3 = 1, 0, a
    x2_1, x2_2, x2_3 = 0, 1, b
    while x2_3 != 0:
        temp = x1_3 // x2_3
        t1, t2, t3 = x1_1 - temp * x2_1, x1_2 - temp * x2_2, x1_3 - temp * x2_3
        x1_1, x1_2, x1_3 = x2_1, x2_2, x2_3
        x2_1, x2_2, x2_3 = t1, t2, t3
    return x1_1 % b

# 加法
def add(P1, P2):
    if P1 == 0:
        return P2
    if P2 == 0:
        return P1
    if P1 != P2:
        lam = (P1[1] - P2[1]) * exgcd(P1[0] - P2[0], p)
    else:
        lam = (3 * P1[0] * P1[0] + a) * exgcd(2 * P1[1], p)

    x = (lam * lam - P1[0] - P2[0]) % p
    y = (lam * (P1[0] - x) - P1[1]) % p
    res = [x, y]
    return res

# 乘法
def multiply(n, P):
    l = len(bin(n)[2:]) - 1
    n = n - 2 ** l
    Z = P
    while l > 0:
        l = l - 1
        Z = add(Z, Z)
    if n > 0:
        Z = add(Z, multiply(n, P))
    return Z

# 用TonelliShanks算法求解二次剩余
def Tonelli_Shanks(n, p):

    # 用Legendre符号判断二次剩余
    def Legendre(n, p):
        return pow(n, (p - 1) // 2, p)

    #assert Legendre(n, p) == 1
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)
    q = p - 1
    s = 0
    while q % 2 == 0:
        q = q // 2
        s += 1
    for z in range(2, p):
        if Legendre(z, p) == p - 1:
            break
    c = pow(z, q, p)
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    if t % p == 1:
        return r
    else:
        i = 0
        while t % p != 1:
            temp = pow(t, 2 ** (i + 1), p)
            i += 1
            if temp % p == 1:
                b = pow(c, 2 ** (m - i - 1), p)
                r = r * b % p
                c = b * b % p
                t = t * c % p
                m = i
                i = 0
        return r

# 将集合中的元素的哈希值映射到椭圆曲线上并求和
def map_elliptic(M):
    # 对于集合中的任一元素，先映射
    x = int(sm3.sm3_hash(list(M)), 16)
    # 已知x,根据定义的椭圆曲线方程求出y,即求解二次剩余，得到点的横纵坐标
    y = Tonelli_Shanks(x * x+ a * x + b, p)
    return [x,y]

def sign(M):
    k = random.randint(1, n - 1)
    R = multiply(k, G)
    e = int(sm3.sm3_hash(add(map_elliptic(M),R)), 16)
    s = (k + e * d) % n
    return R, s ,e

def Verify1(R,s,e):
    if multiply(s, G) == add(R,multiply(e, P)):
        print('验证成功')
    else:
        print('验证失败')


def Verify2(R1,s1,e1):
    s = 0
    for i in s1:
        s = s + i
    e = 0
    for j in e1:
        e = e + j
    R = 0
    for k in R1:
        R = add(R , k)

    if multiply(s, G) == add(R,multiply(e, P)):
        print('验证成功')
    else:
        print('验证失败')

# 椭圆曲线参数
a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
Gx = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
Gy = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2
G = [Gx,Gy]
d = random.randint(1, n - 1)
P = multiply(d, G)

set=[]
for i in range(64):
    M = ''.join(random.sample(string.ascii_letters + string.digits, 8)).encode()
    set.append(M)
R_set=[]
s_set=[]
e_set=[]
for i in set:
    R_,s_,e_=sign(i)
    R_set.append(R_)
    s_set.append(s_)
    e_set.append(e_)

time_start1 = time.time()
for j in range(64):
    Verify1(R_set[j], s_set[j], e_set[j])
time_end1 = time.time()
time_cost1 = (time_end1 - time_start1) * 1000
print(str(time_cost1) + "ms\n")

time_start2 = time.time()
Verify2(R_set,s_set,e_set)
time_end2 = time.time()
time_cost2 = (time_end2 - time_start2) * 1000
print(str(time_cost2)+ "ms\n")



