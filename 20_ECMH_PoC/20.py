from gmssl import sm3
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

# 用TonelliShanks算法求解二次剩余
def Tonelli_Shanks(n, p):

    # 用Legendre符号判断二次剩余
    def Legendre(n, p):
        return pow(n, (p - 1) // 2, p)

    assert Legendre(n, p) == 1
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
def map_elliptic(set):
    set_hash = 0
    for i in set:
        # 对于集合中的任一元素，先映射
        x = int(sm3.sm3_hash(list(i)), 16)
        # 已知x,根据定义的椭圆曲线方程求出y,即求解二次剩余，得到点的横纵坐标
        y = Tonelli_Shanks(x * x+ a * x + b, p)
        # 求和
        set_hash = add(set_hash, [x, y])
    return set_hash

# 椭圆曲线参数
a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
# n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7

set = (b'789', b'567')
set_hash = map_elliptic(set)
print(set_hash)











