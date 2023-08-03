from SM3 import sm3_hash

def birthattack(n):
    precomputed = []
    for k in range(int(2**(n/2))):
        precomputed.append(sm3_hash(bin(k)[2:]+'1'*8))
    for m in range(int(2**(n/2))):
        hash=sm3_hash('1'*8+bin(m)[2:])
        for n in precomputed:
            if hash==n:
                print('存在碰撞，碰撞对应的H(x):', hash,'对应的原像分别为:',(precomputed.index(n),m))

birthattack(32)



