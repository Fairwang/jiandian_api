# !/user/bin/python
# -*- coding: utf-8 -*-

#rsa 加密解密
import rsa
# 先生成一对密钥，然后保存.pem格式文件，当然也可以直接使用
(pubkey,privkey) = rsa.newkeys(2048) #有1024 也有2048
pub = pubkey.save_pkcs1()
print pub
with open('public.pem','w+') as publickfile:
    publickfile.write(pub)
pri = privkey.save_pkcs1()
with open('private.pem','w+') as privatefile:
    privatefile.write(pri)

# 加载公钥和密钥
message = 'Fu128/WbLui9PHoty88BJWutndYL1Sro0OFZei8BdwqQh9h8hxa5RoO87FGbVCLyka1IJbgYNc8xsFT1VR6xO/cYUUqjju0bMLAYfY/CpnQUghzGYPkhKROmtm3dXURtKulCiw8jlMBwIutu8GjZ2bJgESen2RKAacJVwxC0RUI='
with open('public.pem') as publickfile:
    p = publickfile.read()
    pubkey = rsa.PublicKey.load_pkcs1(p)

with open('private.pem') as privatefile:
    p = privatefile.read()
    privkey = rsa.PrivateKey.load_pkcs1(p)

# 用公钥加密、再用私钥解密
crypto = rsa.encrypt(message, pubkey)
message = rsa.decrypt(crypto, privkey)
print crypto
print message

# # sign 用私钥签名认真、再用公钥验证签名
# signature = rsa.sign(message, privkey, 'SHA-1')
# rsa.verify(message, signature, pubkey)

#M2Crypto 加密解密
from M2Crypto import RSA,BIO
#生成公钥私钥
rsa = RSA.gen_key(2048, 3, lambda *agr:None)
pub_bio = BIO.MemoryBuffer()
priv_bio = BIO.MemoryBuffer()
#保存
rsa.save_pub_key_bio(pub_bio)
rsa.save_key_bio(priv_bio,None)
#加载
pub_key = RSA.load_pub_key_bio(pub_bio)
priv_key = RSA.load_key_bio(priv_bio)

message = 'Fu128/WbLui9PHoty88BJWutndYL1Sro0OFZei8BdwqQh9h8hxa5RoO87FGbVCLyka1IJbgYNc8xsFT1VR6xO/cYUUqjju0bMLAYfY/CpnQUghzGYPkhKROmtm3dXURtKulCiw8jlMBwIutu8GjZ2bJgESen2RKAacJVwxC0RUI='
#公钥加密 私钥解密
encrypted = pub_key.public_encrypt(message, RSA.pkcs1_padding)
decrypted = priv_key.private_decrypt(encrypted, RSA.pkcs1_padding)

print decrypted