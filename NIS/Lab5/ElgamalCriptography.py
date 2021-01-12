from Utilities import PrimeNumbers,PowNMod
from PrimitiveRoots import PrimitiveRoots
import random

class ElgamalCriptography:
    def __init__(self):
        self.generateKeys()

    def generateKeys(self):
        prime_length = int(input("How many digits of prime required ? : "))
        PN = PrimeNumbers()
        self.p = PN.GetPrime(prime_length,3)
        PR = PrimitiveRoots()
        self.primitive_roots,self.coprime_list = PR.getPrimitiveRoots(self.p)
        temp_index = random.randint(0,len(self.primitive_roots))
        e_1 = self.primitive_roots[temp_index]
        temp_index = random.randint(0,len(self.coprime_list))
        d = self.coprime_list[temp_index]
        while( d<1 or d>(self.p-1)):
            d = self.coprime_list[temp_index]
        e_2 = PowNMod(e_1,d,self.p)
        self.public_key = (e_1,e_2,self.p)
        self.private_key = d

    def encrypt(self,plain_text):
        pass
    def decrypt(self,cipher_text):
        pass
