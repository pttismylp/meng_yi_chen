import random
from gmssl import sm3
import socket
import json
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


a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
Gx = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
Gy = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2
G = [Gx,Gy]

ID_A = 0x3AFC567D839B4982113C564472215DC973B7
ID_B = 0xF35A3C44718294C93BD84A9366C99E9F3A74
message = "message"

HOST = '192.168.0.104'
PORT = 22342
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

#（1）Generate sub private key d1,compute P1
d1 = random.randint(1, n)
P1 = multiply(gmpy2.invert(d1,p),G)

s.send(str(P1).encode())
P_1 = s.recv(1024).decode()
P = json.loads(P_1)

#（3）
M = message.encode()
ENTLA = len(hex(ID_A)[2:]) #ID_A的长度
ENTLB = len(hex(ID_B)[2:]) #ID_B的长度
z = ENTLA.to_bytes((ENTLA.bit_length() + 7) // 8, 'big') + ID_A.to_bytes((ID_A.bit_length() + 7) // 8,'big') + ENTLB.to_bytes((ENTLB.bit_length() + 7) // 8, 'big') + ID_B.to_bytes((ID_B.bit_length() + 7) // 8, 'big') + a.to_bytes((a.bit_length() + 7) // 8, 'big') + b.to_bytes((b.bit_length() + 7) // 8, 'big') + Gx.to_bytes((Gx.bit_length() + 7) // 8, 'big') + Gy.to_bytes((Gy.bit_length() + 7) // 8, 'big') + P[0].to_bytes((P[0].bit_length() + 7) // 8, 'big') + P[1].to_bytes((P[1].bit_length() + 7) // 8, 'big')
Z = int(sm3.sm3_hash(list(z)), 16)
M1 = Z.to_bytes((Z.bit_length() + 7) // 8, 'big') + M
e = int(sm3.sm3_hash(list(M1)), 16)
k1 = random.randint(1, n)
Q1 = multiply(k1,G)

s.send(str(Q1).encode())
s.send(str(e).encode())
rs = s.recv(1024).decode()
r, s2, s3 = json.loads(rs)

#（5）Generate signature (r, s)
ss = (d1 * k1 * s2 + d1 * s3 - r) % n
print("signature:",(r,ss))


