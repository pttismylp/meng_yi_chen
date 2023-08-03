import random
from gmssl import sm3
import socket
import json
import gmpy2

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

def KDF(z,klen):
    ct=1
    k=''
    for i in range(int(klen/256)+1):
        k=k+sm3.sm3_hash(list(z+ct.to_bytes(4,byteorder='big', signed=False)))
        ct=ct+1
    k='0'*((256-(len(bin(int(k,16))[2:])%256))%256)+bin(int(k,16))[2:]
    return int(hex(int(k[:klen],2))[2:],16)

k = random.randint(1, n)
message = "message"
print("明文:",message)
M = message.encode()
def enc(G,P):
    C1 = multiply(k, G)
    x2, y2 = multiply(k, P)
    t = KDF(x2.to_bytes((x2.bit_length() + 7) // 8, 'big') + y2.to_bytes((y2.bit_length() + 7) // 8, 'big'), len(M) * 8)
    C2= int.from_bytes(M,'big') ^ t
    C3 = int(sm3.sm3_hash(list(x2.to_bytes((x2.bit_length() + 7) // 8, 'big') + M + y2.to_bytes((y2.bit_length() + 7) // 8, 'big'))), 16)
    return C1,C2,C3

HOST = '192.168.0.104'
PORT = 22344
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

d1 = random.randint(1, n)
P1 = multiply(gmpy2.invert(d1,p),G)
s.send(str(P1).encode())
P_1 = s.recv(1024).decode()
P = json.loads(P_1)

# Encrypt
C1, C2, C3 = enc(G, P)
C = C1[0].to_bytes((C1[0].bit_length() + 7) // 8, 'big') + C1[1].to_bytes((C1[1].bit_length() + 7) // 8, 'big') + C2.to_bytes((C2.bit_length() + 7) // 8, 'big') + C3.to_bytes((C3.bit_length() + 7) // 8, 'big')
if C1 != [0,0]:
    T1 = multiply(gmpy2.invert(d1,p),C1)
s.send(str(T1).encode())

T2_1 = s.recv(1024).decode()
T2 = json.loads(T2_1)
(x2,y2)=add(T2,sym_node(C1))
t = KDF(x2.to_bytes((x2.bit_length() + 7) // 8, 'big') + y2.to_bytes((y2.bit_length() + 7) // 8, 'big'), len(M) * 8)
M2 = C2 ^ t
u = int(sm3.sm3_hash(list(x2.to_bytes((x2.bit_length() + 7) // 8, 'big') + M2.to_bytes((M2.bit_length() + 7) // 8, 'big') + y2.to_bytes((y2.bit_length() + 7) // 8, 'big'))), 16)
if u == C3:
    print("解密:",M2.to_bytes((M2.bit_length() + 7) // 8, 'big').decode())
