'''
Author : Dhruv B Kakadiya

'''
import random as rd
from math import sqrt

def getPrimeFactors(n):
        factors = []
        # If 2 is a factor
        if (not n & 1):
            factors.append(2)

        while (not n & 1):
            n = n >> 1

        # If prime > 2 is factor
        for i in range(3, int(sqrt(n)) + 1, 2):
            if (n % i == 0):
                factors.append(i)
                while (n % i == 0):
                    n = n // i
        if (n > 1):
            factors.append(n)

        return factors

def getPrimitiveRoot(p):
        factors = getPrimeFactors(p-1)
        ans = -1
        for _ in range(10**3):
            n = rd.randint(2, p-1)
            l = len(factors)
            for i in factors:
                if pow(n, (p-1)//i, p) != 1:
                    l -= 1
                else:
                    break
            if l == 0:
                ans = n
        return ans

# phi function
def phi (n):
    return (n - 1)

def find_mul_inverse (a, n):
    t1, t2 = 0, 1
    mod = n
    while(a > 0):
        q = n // a
        r = n - (q * a)
        n, a = a, r
        t = t1 - (q * t2)
        t1, t2 = t2, t
    _, t = n, t1
    if (t < 0):
        t %= mod
    return (t)

# multiply and square function
def multiply_and_square(a, x, n):
    x = bin(x)
    x = x[2 : ]
    x = x[:: -1]
    y = 1
    for i in range(0, len(x)):
        if (int(x[i]) == 1):
            y = (y * a) % n
        a = (a ** 2) % n
    return y

# find public and private keys
def find_public_private_key (proots, prime):
    e1 = proots[rd.randint(0, len(proots) - 1)]
    condition = prime - 2
    while (True):
        r = rd.randint(0, len(proots) - 1)
        d = proots[r]
        if (d <= condition):
            break
    e2 = multiply_and_square (e1, d, prime)
    return (e1, e2, prime)

def find_s1 (e1, r, p, q):
    return (((e1 ** r) % p) % q)

def find_s2 (plain_text, d, s1, r, q, p):
    inv = find_mul_inverse(r, q)
    #print(f"inverse is = >  {inv}")
    return (((plain_text + (d * s1)) * inv) % q)

def find_t1 (s1, s2, e1, e2, plain_text, p, q):
    #return (((e1 ** (plain_text * find_mul_inverse(s2, q))) * (e2 ** (s1 * find_mul_inverse(s2, q)))) % p) % q
    return  ((( e1 ** ((plain_text * find_mul_inverse(s2, q)) % q)) * ( e2 ** ((s1 * find_mul_inverse(s2, q)) % q ))) % p ) % q
    #return  (( e1 ** ((plain_text * find_mul_inverse(s2, q)) % q)) * ((( e2 ** ((s1 * find_mul_inverse(s2, q)) % q ))) % p)) % q

# main if condition
if __name__ == "__main__":
    #n = int(input("\nEnter the number of bits of prime number :- "))
    p, q = map(int, (input("Enter two prime number :- ")).split())

    # finding public and private key
    e0 = getPrimitiveRoot(p)
    print(f"\n e0 is => {e0}")
    e1 = pow(e0, ((p - 1) // q), p)
    d = rd.randint(1, q - 1)
    r = int(input("\nEnter random 'r' as per GCD(r, q) = 1 => "))
    e2 = (e1 ** (d)) % p

    print(f"\nPublic key is => '{e1}', '{e2}', '{p}', '{q}'")
    print(f"\nprivate key is => '{d}'")
    print(f"\nr is => {r}")
    plain_text = int(input("\nEnter M :- "))

    s1 = find_s1 (e1, r, p, q)
    s2 = find_s2 (plain_text, d, s1, r, q, p)
    t1 = find_t1 (s1, s2, e1, e2, plain_text, p, q)
    t2 = s1

    print(f"\nS1 is => {s1}")
    print(f"\nS2 is => {s2}")
    print(f"\nt1 is => {t1}")
    print(f"\nt2 is => {t2}")

    if (t1 == t2):
        print("Valid Sender!")
    else:
        print("SCAM")