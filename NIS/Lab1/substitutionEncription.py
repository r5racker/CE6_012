# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 16:12:31 2020

@author: RAHIL
"""


class SubstitutionCription:

    def __init__(self,secretKey):
        self.secretKey = secretKey
        
    def encrypt(self,plainText):
        plainText = plainText.lower()
        cript = []
        
        for c in plainText :
            delta = ord(c) - ord('a')
            cip = self.secretKey[delta]
            cript.append(cip)
        return ''.join(cript)
    
    def decrypt(self,cipher):
        plainText = []
        base = ord('a')
        for c in cipher :
            delta = self.secretKey.index(c)
            cip = chr(base + delta)
            plainText.append(cip)
        return ''.join(plainText)
    
if(__name__ == "__main__"):
    testKey = ["z","x","c","v","b","n","m","a","s","d","f","g","h","j","k","l","q","w","e","r","t","y","u","i","o","p"]
    testText = input("Plain Text: ")
    Cripter = SubstitutionCription(testKey)
    cipher = Cripter.encrypt(testText)
    print("string :",testText)
    print("key :",testKey)
    print("encrypted :",cipher)
    print("decripted : ",Cripter.decrypt(cipher))