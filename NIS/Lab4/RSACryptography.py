import random
from Utilities.PowerNMode import PowNMod
from Utilities.EuclidianExtended import EuclidianExtended
class RSACryptography:
    def __init__(self):
        super().__init__()
        self.PublicKey, self._PrivateKey, self.N = self.__GenKeys()

    def millerRabinTest(self,n):
        d=n-1
        while (d % 2 == 0): 
            d //= 2 
        # Miller Rabin Test
        a = 2 + random.randint(1, n - 4) 
        #a^d % n 
        x = PowNMod(a, d, n) 
    
        if (x == 1 or x == n - 1): 
            return True 
        while (d != n - 1): 
            x = (x * x) % n 
            d *= 2 
    
            if (x == 1): 
                return False 
            if (x == n - 1): 
                return True 
        return False

    def isPrime(self,n,accuracyFactor):
        
        # Corner cases 
        if (n <= 1 or n == 4): 
            return False 
        if (n <= 3): 
            return True 
        # Iterate given nber of 'k' times 
        for _ in range(accuracyFactor): 
            if (self.millerRabinTest( n) == False): 
                return False 
        return True

    def __GetPrime(self,prime_len,accuracyFactor =3):
        
        #prime = int(input("Enter Prime number : "))
        prime = random.randint(10**(prime_len-1),10**prime_len)

        while not self.isPrime(prime,accuracyFactor):
            prime = random.randint(10**(prime_len-1),10**prime_len)
        print("prime",prime)
        return prime

    def __GenKeys(self):
        '''
            Return : publicKey, privateKey
        '''
        prime_len = int(input("How many digit prime? : "))
        p, q = self.__GetPrime(prime_len), self.__GetPrime(prime_len)

        while(p == q):
            q = self.__GetPrime(prime_len)

        n = p*q
        phiN = (p-1)*(q-1)
        # public key
        e = random.randint(2, phiN - 1)
        EE = EuclidianExtended()
        while(EE.GetGcd(e, phiN) != 1):
            e = random.randint(2, phiN - 1)
        # private key
        d = EE.GetInv(e, phiN)  # d := (e^-1 MOD phiN)
        #print("keys",e,d,n)
        return e, d, n

    def Encrypt(self, plainText):
        base = ord('a')
        cipherList = []
        for pChar in plainText:
            M = ord(pChar) - base
            # pow(M, self.publicKey) % self.N  # power & mod
            cipherChar = PowNMod(M, self.PublicKey, self.N)
            cipherList.append(cipherChar)
            #cipherText += chr(cipherChar)

        return cipherList

    def Decrypt(self, cipherText):
        base = ord('a')
        plainText = ""
        for cChar in cipherText:
            C = cChar
            # pow(C, self.privateKey) % self.N  # power & mod
            plainChar = PowNMod(C, self._PrivateKey, self.N)
            #print(base+plainChar,"N:",self.N)
            plainText += chr(base+plainChar)
        return plainText


RSAC = RSACryptography()
plainText = "helloworld"
cipher = RSAC.Encrypt(plainText)
plainDecrypted = RSAC.Decrypt(cipher)

print("plain text :", plainText)
print("public,private :", RSAC.PublicKey, RSAC._PrivateKey)
print("Cipher : ", cipher)
print("decrypted text : ", plainDecrypted)
