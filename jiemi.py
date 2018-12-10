# !/user/bin/python
# -*-coding:utf-8-*-
from M2Crypto import RSA, BIO
import base64
#公钥加密 私钥解密
private_key_str = file('rsa_private.pem', 'rb').read()
print private_key_str
private_key = RSA.load_key_string(private_key_str)
print private_key
data = base64.decodestring('Fu128/WbLui9PHoty88BJWutndYL1Sro0OFZei8BdwqQh9h8hxa5RoO87FGbVCLyka1IJbgYNc8xsFT1VR6xO/cYUUqjju0bMLAYfY/CpnQUghzGYPkhKROmtm3dXURtKulCiw8jlMBwIutu8GjZ2bJgESen2RKAacJVwxC0RUI=')
print "data :%s " %data
de_data = private_key.private_decrypt(data, RSA.pkcs1_padding)
print de_data

