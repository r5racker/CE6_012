import random


def PowNMod(base, power, mod):
    res = 1     # Initialize result

    # Update base if it is more
    # than or equal to mod
    base = base % mod
    if (base == 0):
        return 0
    while (power > 0):
        # If power is odd, multiply
        # base with result
        if ((power & 1) == 1):
            res = (res * base) % mod
        # power must be even now
        power = power >> 1      # power = power/2
        base = (base * base) % mod
    return res


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


class RSACryptography:
    def __init__(self):
        super().__init__()
        self.PublicKey, self._PrivateKey, self.N = self.__GenKeys()

    def __GetPrime(self):
        prime = int(input("Enter Prime number : "))
        return prime

    def __GenKeys(self):
        '''
            Return : publicKey, privateKey
        '''
        p, q = self._GetPrime(), self._GetPrime()

        while(p == q):
            q = __GetPrime()

        n = p*q
        phiN = (p-1)*(q-1)
        # public key
        e = random.randint(2, phiN - 1)
        EE = EuclidianExtended()
        while(EE.GetGcd(e, phiN) != 1):
            e = random.randint(2, phiN - 1)
        # private key
        d = EE.GetInv(e, phiN)  # d := (e^-1 MOD phiN)
        return e, d, n

    def Encrypt(self, plainText):
        base = ord('a')
        cipherText = ""
        cipherList = []
        for pChar in plainText:
            print(pChar)

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
