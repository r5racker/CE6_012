from DSS_Elgamal import find_mul_inverse
from math import ceil, sqrt
from random import randint

class EllipticalCurve:
    def __init__(self, a, b, prime):
        self.a = a
        self.b = b
        self.prime = prime
        self.isValid()
        self.all_points = []

    def power_nmod (self, a, n, prime):
        res = 1
        a %= prime
        if (a == 0):
            return (0)
        while (n > 0):
            if ((n & 1) == 1):
                res = (res * a) % prime
            n >>= 1
            a = (a ** 2) % prime
        return (res)

    def isValid(self):
        if ( (4 * self.a ** 3) + (27 * self.b ** 2) == 0):
            print("Invalid Combination of a and b!")
            return (False)
        else:
            print("Valid combination of a and b!")
            return (True)

    def getPoints(self):
        if(self.isValid()):
            x = 0
            all_points = []
            while (x < self.prime):
                w = (x ** 3 + self.a * x + self.b) % self.prime
                if( self.power_nmod(w, ((self.prime - 1) // 2), self.prime) == 1 ):
                    root = sqrt(w)
                    while (ceil(root) != root):
                        w += self.prime
                        root = sqrt(w)
                    all_points.append((x, int(root % self.prime)))
                    all_points.append((x, int((-root) % self.prime)))
                if(self.power_nmod(w, (self.prime - 1) // 2, self.prime) == self.prime - 1 ):
                    #print(f"No Solution for {x}!")
                    pass
                x += 1
            self.all_points = all_points
            return (all_points)
        else:
            return ([])

    def getRandomPoint(self):
        if(self.all_points == []):
            self.getPoints()
        index = randint(0, len(self.all_points))
        return (self.all_points[index])

    def find_s1 (self, pp, q):
        return (pp[0] % q)

    def find_s2 (self, M, d, s1, r, q):
        return ((M + (d * s1)) * find_mul_inverse(r, q)) % q

    def find_AB (self, M, s1, s2, q):
        A = (M * find_mul_inverse(s2, q)) % q
        B = (s1 * find_mul_inverse(s2, q)) % q
        return A, B


if __name__ == "__main__":
    a, b = 2, 3
    # p, q = 624451, 181
    # p ,q = 191, 19
    p, q = 10099, 7757
    # take private key
    d = 8
    print(f"\nd is => {d}")
    ec = EllipticalCurve(a, b, p)
    points = ec.getPoints()
    print(f"\npoints are => {points}")
    e1 = points[randint(0, len(points))]
    print(f"\ne1 is => {e1}")
    e2 = (d * (e1[0]), d * (e1[1]))
    print(f"\ne2 is => {e2}")

    # signing part
    r = randint(1, q - 1)
    print(f"\nr is => {r}")
    pp = (r * (e1[0]), r * (e1[1]))
    print(f"\npp is => {pp}")
    s1 = ec.find_s1(pp, q)
    print(f"\ns1 is => {s1}")
    dic = []
    for i in range(100):
        M = i
        s2 = ec.find_s2(M, d, s1, r, q)
        print(f"\ns2 is => {s2}")
        A, B = ec.find_AB (M, s1, s2, q)
        print(f"\nA, B is => {A}, {B}")
        T = ((A * e1[0]) + (B * e2[0]), (A * e1[1]) + (B * e2[1]))
        print(f"\nT is => {T[0] % q}, s1 % q => {s1 % q}")
        if ((T[0] % q) == (s1 % q)):
            dic.append(i)
    print(dic)
    print(len(dic))
    # a, b = 1, 1
    # prime = 13
    # ec = EllipticalCurve(a, b, prime)
    # print(ec.getPoints())