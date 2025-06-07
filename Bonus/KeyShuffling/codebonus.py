#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flag import FLAG

def xor(u, v):
    return ''.join(chr(ord(cu) ^ ord(cv)) for cu, cv in zip(u, v))


u = FLAG
v = FLAG[1:] + FLAG[0]

enc = open('flag.enc', 'wb')
flag_enc = xor(u, v)
enc.write(flag_enc.encode('utf-8'))
enc.close()

"""
FLAG = 0102030405060708
u = 0102030405060708
v = 0203040506070801

"""