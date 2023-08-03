import hmac
import hashlib
import random
from gmssl import sm2, sm3, func
import math
import gmpy2

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

# 对称点
def sym_node(G):
    Gx = G[0]
    Gy = p-G[1]
    return [Gx,Gy]

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

    # assert Legendre(n, p) == 1
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

def k_RFC6979(message_, x):
    h1 = sm3.sm3_hash(func.bytes_to_list(message_))
    bh1 = bytes(h1, encoding="utf-8")
    bx = bytes(x, encoding='utf-8')
    v = b'\x01' * 32
    k = b'\x00' * 32
    k = hmac.new(k, v + b'\x00' + bx + bh1, hashlib.sha256).digest()
    v = hmac.new(k, v, hashlib.sha256).digest()
    k = hmac.new(k, v + b'\x01' + bx + bh1, hashlib.sha256).digest()
    v = hmac.new(k, v, hashlib.sha256).digest()
    return int.from_bytes(hmac.new(k, v, hashlib.sha256).digest(), "big") % p

a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
Gx = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
Gy = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2
G = [Gx,Gy]
dA = random.randrange(1, n)
PA = multiply(dA, G)

IDA = 0x3AFC567D839B4982113C564472215DC973B7
message="message"
message_bytes=b"message"

# Precompute
ENTLA = len(hex(IDA)[2:])
to_hash = ENTLA.to_bytes(2, 'big') + IDA.to_bytes((IDA.bit_length() + 7) // 8, 'big') + a.to_bytes((a.bit_length() + 7) // 8,
                                                                                             'big') + b.to_bytes(
    (b.bit_length() + 7) // 8, 'big') + Gx.to_bytes((Gx.bit_length() + 7) // 8, 'big') + Gy.to_bytes(
    (Gy.bit_length() + 7) // 8, 'big') + PA[0].to_bytes((PA[0].bit_length() + 7) // 8, 'big') + PA[1].to_bytes(
    (PA[1].bit_length() + 7) // 8, 'big')
ZA = int(sm3.sm3_hash(list(to_hash)), 16)

# Sign
def sm2_RFC6979_sign(message,message_bytes):
    M1 = ZA.to_bytes((ZA.bit_length() + 7) // 8,'big') + message.encode()
    e=int(sm3.sm3_hash(list(M1)),16)
    k = k_RFC6979(message_bytes,str(hex(dA)[2:]))%n
    x1,y1 = multiply(k, G)
    r = (e+x1)%n
    s = (exgcd(1+dA,n)*(k-r*dA))%n
    return e,r,s

def deduce_publickey_from_signature(e,r,s):
    x1 = (r - e) % n
    y1 = Tonelli_Shanks(x1 * x1+ a * x1 + b, p)
    kG = [x1,y1]
    PA = multiply(gmpy2.invert((s+r),p),add(kG,sym_node(multiply(s,G))))
    return PA

e,r,s = sm2_RFC6979_sign(message,message_bytes)
print("签名：",r,s)
PA = deduce_publickey_from_signature(e,r,s)
print('公钥为：',PA)