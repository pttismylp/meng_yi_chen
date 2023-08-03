import random
import socket
import gmpy2
import json
from gmssl import sm3

def powermod(x,y,z):
    x = x % z
    ans = 1
    while y != 0:
        if y & 1:
            ans = (ans*x)%z
        y >>= 1
        x = (x*x) % z
    return ans

u_ = 'myc'
p_ = '202100460081'
HOST = '192.168.0.104'
PORT = 33333
p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
s = socket.socket()
s.connect((HOST, PORT))
address = ('192.168.0.104', 33333)

# Client generate ephemeral secret key
a = random.randint(1, n)
# Client compute key-value
h = sm3.sm3_hash(list(u_.encode() + p_.encode()))
k = h[:2]
v = powermod(int(h, 16), a, p)

s.send(k.encode())
s.send(str(v).encode())

json_string, addr = s.recvfrom(2048)
# Username and password detection
if json_string.decode() == '':
    print("Secure.")
else:
    S = json.loads(json_string)
    h_ab = int(s.recv(1024).decode())
    h_b = powermod(h_ab, gmpy2.invert(a, p), p)
    if h_b in S:
        print("Insecure.")
    else:
        print("Secure.")
