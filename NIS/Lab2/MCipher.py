# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 16:18:57 2020

@author: RAHIL
"""
from EuclidianExtended import EuclidianExtended as EExtended

class MCipher:
    
    def __init__(self,k1,n):
        print("Using Multiplicative cipher")
        self.key1 = k1
        #self.key2 = k2
        self.mod = n
        self.base = ord('a')
    def encrypt(self, plainText):
        crypt = ""
        for c in plainText:
            delta = ( (ord(c) - ord('a')) * self.key1 )%self.mod 
            crypt += chr(self.base + delta)
        return crypt
    
    def decrypt(self, crypt):
        InvGen = EExtended()
        plain = ""
        gcd,inv = InvGen.run(self.key1, self.mod)
        for c in crypt:
            delta = ( ((ord(c)-ord('a')))*inv )%self.mod 
            plain += chr(self.base + delta)
        return plain
print(__name__)
if(__name__ == "__main__"):
    k1,n = list(map(int,input("enter key & numberOfCharacters : ").split()))
    MCrypter = MCipher(k1, n)
    for _ in range(int(input("number of test case : "))):
        plain = input("Plain text: ")
        cipher = MCrypter.encrypt(plain)
        print("cipher : ",cipher)
        print("plain text(decrypted) : ",MCrypter.decrypt(cipher))
