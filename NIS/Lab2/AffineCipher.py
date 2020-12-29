# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 16:18:57 2020

@author: RAHIL
"""
from EuclidianExtended import EuclidianExtended as EExtended


class AffineCipher:
    def __init__(self, k1, k2, n):
        self.key1 = k1
        self.key2 = k2
        self.mod = n
        self.base = ord('a')

    def encrypt(self, plainText):
        crypt = ""
        for c in plainText:
            delta = ((ord(c) - ord('a')) * self.key1 + self.key2) % self.mod
            crypt += chr(self.base + delta)
        return crypt

    def decrypt(self, crypt):
        InvGen = EExtended()
        plain = ""
        gcd, inv = InvGen.run(self.key1, self.mod)
        for c in crypt:
            delta = (((ord(c)-ord('a'))-self.key2)*inv) % self.mod
            plain += chr(self.base + delta)
        return plain


print(__name__)
if(__name__ == "__main__"):
    k1, k2, n = list(
        map(int, input("key1 key2 numberOfCharacters : ").split()))
    ACrypter = AffineCipher(k1, k2, n)
    for _ in range(int(input("Number of test cases : "))):
        plain = input("Plain Text : ")
        cipher = ACrypter.encrypt(plain)
        print("cipher : ", cipher)
        print("deciphered Text : ", ACrypter.decrypt(cipher))
