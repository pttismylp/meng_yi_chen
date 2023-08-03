import base64
import binascii
from gmssl import sm2, func
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT

private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'

# 加密
def pgp_enc(m):
    print("明文为：",m)
    # 会话密钥
    key = b'3l5butlj26hvv313'
    # SM4加密明文
    crypt_sm4 = CryptSM4()
    crypt_sm4.set_key(key, SM4_ENCRYPT)
    c = crypt_sm4.crypt_ecb(m)
    print("密文为：",c)
    # SM2加密会话密钥
    sm2_crypt = sm2.CryptSM2(public_key=public_key, private_key=private_key)
    enc_key = sm2_crypt.encrypt(key)
    return enc_key,c

# 解密
def pgp_dec(enc_key,c):
    # 先用SM2解密会话密钥
    sm2_crypt = sm2.CryptSM2(public_key=public_key, private_key=private_key)
    key =sm2_crypt.decrypt(enc_key)
    # 再利用SM4通过解密出来的会话密钥对明文进行解密
    crypt_sm4 = CryptSM4()
    crypt_sm4.set_key(key, SM4_DECRYPT)
    m = crypt_sm4.crypt_ecb(c) #  bytes类型
    print("解密结果为：",m)

m = b"message"
enc_key,c=pgp_enc(m)
pgp_dec(enc_key,c)