#!/usr/bin/env python
#coding:UTF-8
import hashlib
import hmac

sk = "sk"
msg = "2"

def get_authorization(sk, msg):  
    hashing = hmac.new(sk, msg, hashlib.sha1).hexdigest()  
    return hashing  
  
def test():
    print get_authorization(sk, msg) 

if __name__ == '__main__':
    test()
