import gmpy2
import random
import math

a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
Gx = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
Gy = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2
G = [Gx,Gy]

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

def Sign(d, m, G):
    r1= multiply(k, G)[0] % n
    s1 = ((hash(m) + d * r1)*gmpy2.invert(k, n)) % n
    return r1, s1

def Verify(m, r, s):
    v1 = (hash(m) * gmpy2.invert(s, n)) % n
    v2 = (r * gmpy2.invert(s, n)) % n
    res = add(multiply(v1, G), multiply(v2, P))
    if res == 0:
        print('Validation failed')
    else:
        if r == res[0] % n:
            print('succeeded')
        else:
            print('failed')

# Leaking k leads to leaking of d
def leaking(m, r, s,d):
    print("Leaking k leads to leaking of d:")
    d1 = gmpy2.invert(r, n) * (k * s - hash(m)) % n
    if d == d1:
        print('succeeded')
    else:
        print('failed')

# Reusing k leads to leaking of d
def reusing(m, r1, s1, m_, r2, s2,d):
    print("Reusing k leads to leaking of d:")
    d1 = ((s1 * hash(m_) - s2 * hash(m)) * gmpy2.invert(s2 * r1 - s1 * r2, n)) % n
    if d == d1:
        print('succeeded')
    else:
        print('failed')

# Two users, using k leads to leaking of d, that is they can deduce each other’s d
def deduce_d(r, s1, m, d1, s2, m_, d2):
    print("Two users, using k leads to leaking of d, that is they can deduce each other’s d:")
    d11 = ((s1 * hash(m_) - s2 * hash(m) + s1 * r * d2) * gmpy2.invert(s2 * r, n)) % n
    d21 = ((s2 * hash(m) - s1 * hash(m_) + s2 * r * d1) * gmpy2.invert(s1 * r, n)) % n
    if d1 == d11 and d2 == d21:
        print("succeeded")
    else:
        print("failed")

# One can forge signature if the verification does not check m
def forge_sign():
    print("One can forge signature if the verification does not check m:")
    u = random.randint(1, n - 1)
    v = random.randint(1, n - 1)
    r1 = add(multiply(u, G), multiply(v, P))[0]
    e1 = (r1 * u * gmpy2.invert(v, n)) % n
    s1 = (r1 * gmpy2.invert(v, n)) % n
    res = add(multiply((e1 * gmpy2.invert(s1, n)) % n, G), multiply((r1 * gmpy2.invert(s1, n)) % n, P))
    if res == 0:
        print('failed')
    else:
        if r1 == res[0] % n :
            print('succeeded')

        else:
            print('failed')

m = 'user1'
m_ = 'user2'
k = random.randint(1, n)
d = random.randint(1, n)
P = multiply(d, G)
r1, s1 = Sign(d, m, G)
print('ECDSA:')
leaking(m, r1, s1, d)
r2, s2 = Sign(d, m_, G)
reusing(m, r1, s1, m_, r2, s2, d)
r3, s3 = Sign(gmpy2.invert(d,p),m,G)
deduce_d(r1, s2, m_, d, s3, m, gmpy2.invert(d,p))
print("Malleability (r, −s) is valid signatures:")
print('verify(r,s)：')
Verify(m, r1, s1)
print('verify(r,-s)：')
Verify(m, r1, -s1)
forge_sign()