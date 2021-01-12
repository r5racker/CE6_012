import random
class PrimeNumbers:
    def PowNMod(self,base, power, mod):
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

    def millerRabinTest(self,n):
        d=n-1
        while (d % 2 == 0): 
            d //= 2 
        # Miller Rabin Test
        a = 2 + random.randint(1, n - 4) 
        #a^d % n 
        x = self.PowNMod(a, d, n) 
    
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

    def GetPrime(self,prime_len,accuracyFactor =3):
        
        #prime = int(input("Enter Prime number : "))
        prime = random.randint(10**(prime_len-1),10**prime_len)

        while not self.isPrime(prime,accuracyFactor):
            prime = random.randint(10**(prime_len-1),10**prime_len)
        print("prime",prime)
        return prime