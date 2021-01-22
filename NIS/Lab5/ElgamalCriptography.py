from MyUtilities import PrimeNumbers,PowNMod,EuclidianExtended
from PrimitiveRoots import PrimitiveRoots
import random
import time

class ElgamalCriptography:
    def __init__(self,base=0):
        self.base = base
        self.generateKeys()

    def generateKeys(self):
        prime_length = int(input("How many digits of prime required ? : "))
        PN = PrimeNumbers()
        self.p = PN.GetPrime(prime_length,3)
        PR = PrimitiveRoots()
        start_time = time.time()
        self.primitive_roots,self.coprime_list = PR.getPrimitiveRoots(self.p)
        print("primitive Roots:")
        print(self.primitive_roots)
        end_time = time.time()
        print("_____________")
        print("time taken in primitive root generation (sec): %1.3f"%(end_time - start_time))
        temp_index = random.randint(0,len(self.primitive_roots))
        e_1 = self.primitive_roots[temp_index]
        temp_index = random.randint(0,len(self.coprime_list))
        d = self.coprime_list[temp_index]
        while( d<1 or d>(self.p-1)):
            print("d",d)
            d = self.coprime_list[temp_index]
        e_2 = PowNMod(e_1,d,self.p)
        self.publiC_key = (e_1,e_2,self.p)
        self.private_key = d
        print("keys Generated")

    def encrypt(self,plain_text):
        cipherList = []
        base = self.base
        print("Encrypting text")
        for pChar in plain_text:
            M = ord(pChar) - base
            temp_index = random.randint(0,len(self.coprime_list))
            r = self.coprime_list[temp_index]
            C_1 = PowNMod(self.publiC_key[0],r,self.p)
            C_2 = (PowNMod(self.publiC_key[1],r,self.p) * M )%self.p
            cipherList.append((C_1,C_2))
        return cipherList

    def decrypt(self,cipher_text):
        EE = EuclidianExtended()
        base=self.base
        plainText = ""
        for cChar in cipher_text:
            C_1,C_2 = cChar
            C_1_inv = EE.GetInv(PowNMod(C_1, self.private_key, self.p),self.p)
            plainChar = (C_2 * C_1_inv) %self.p
            plainText += chr(base+plainChar)
        return plainText
    def test(self):    
        plain_text = "Hello World"
        cipher = self.encrypt(plain_text)
        decrypted_text = self.decrypt(cipher)
        print(f"plain Text : {plain_text}")
        print(f"Public Key : {self.publiC_key}")
        print(f"private key : {self.private_key}")
        print(f"cipher text : {cipher}")
        print(f"decrypted Text : {decrypted_text}")
if __name__ == "__main__":
    EC = ElgamalCriptography(0)
    EC.test()