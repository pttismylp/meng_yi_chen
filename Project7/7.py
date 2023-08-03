from sm2 import CryptSM2
import pysmx
import random
import gmssl
import hashlib

sk = '512DF8223233092282FFA58E6CC630D22AB8B77844A570DAAEFF77DCCFAF0D78'
pk = 'A50EF35C343A67E8DA535AE86603BA4992E32FED2857A48A37AE665F988B6EB5FEF82C122D385434C58344B2852D595D19E6FF0F57558FA085D3618EF6E86A32'
tans = random.randrange(1000000000)

def toh(oxe):
    x = hashlib.sha256()
    x.update(oxe.encode())
    return x.hexdigest()

def Verify(signature,n,cre,v):
    if n <= 0:
        t = v
    else:
        t = toh(v)
    for i in range(n-1):
        t = toh(t)
    if t == cre:
        if CryptSM2(public_key=pk, private_key=sk).verify(signature, tans):
            return True
        else:
            return False
    else:
        return False

def Sign(n,m):
    h = pysmx.SM3.hash_msg(str(random.getrandbits(256)))
    if m <= 0:
        ans = h
    else:
        ans = toh(h)
    if n > 0:
        u = toh(h)
    else:u = h
    for i in range(m-1):
        ans = toh(ans)
    for i in range(n-1):
        u = toh(u)
    sm2_ = CryptSM2(public_key=pk, private_key=sk)
    signature = sm2_.sign(tans, gmssl.func.random_hex(sm2_.para_len))
    return u, ans, signature

def parb(digit):
    list = []
    for i in range(3):
        l = random.randrange(100000)
        list.append(l)
    if digit < list[1]:g = list[1]
    elif digit > list[2]:
        g = list[0]
    else:
        g = list[2]
    u1, ans1, signature1 = Sign(g % 10 - (digit % 10),g % 10)
    u2, ans2, signature2 = Sign(g//100-(digit//100),g//100)
    u3, ans3, signature3 = Sign(g // 10 - 10 * (g // 100) - (digit // 10 - 10 * (digit // 100)),g // 10 - 10 * (g // 100),)
    if Verify(signature3,digit//10-10*(digit//100),ans3,u3) == True:
        if Verify(signature2,digit//100,ans2,u2) == True:
            if Verify(signature1,digit%10,ans1,u1) == True:
                return True
            else:
                return False
    else:
        return False


if parb(300) == True:
    print('Succeed.')