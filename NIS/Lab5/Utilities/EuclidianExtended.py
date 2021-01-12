# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 15:33:19 2020

@author: RAHIL
"""

class EuclidianExtended:
    def __init__(self):
        pass

    def run(self, a, n):
        r1 = n
        r2 = a
        t1 = 0
        t2 = 1
        while r2 > 0:
            q = r1//r2
            r = r1 % r2
            r1 = r2
            r2 = r
            t = t1 - q*t2
            t1 = t2
            t2 = t
        gcd = r1
        inv = t1
        if(gcd < 0):
            gcd += n
        if(inv < 0):
            inv += n
        if(gcd != 1):
            inv = -1
        return gcd, inv

    def GetGcd(self, a, n):
        gcd, _ = self.run(a, n)
        return gcd

    def GetInv(self, a, n):
        _, inv = self.run(a, n)
        return inv


if(__name__ == "__main__"):
    EExtended = EuclidianExtended()
    for _ in range(int(input("Number of Test Cases: "))):
        a, n = list(map(int, input("a n : ").split()))
        gcd, inv = EExtended.run(a, n)
        print("gcd: ", gcd, "inverse: ", inv)
        print("_____________")
