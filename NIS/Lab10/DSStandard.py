'''
digital signature standard
=>  elgamal + schnorr scheme
'''
from Utilities import PrimeNumbers,PowNMod,EuclidianExtended
from random import randint

class DSS_elgamal_schnorr:
    def __init__(self,prime_length):
        self.p_numbers = PrimeNumbers()
        self.p = self.p_numbers.GetPrime(prime_length)
        self.q = max(self.p_numbers.getPrimeFactors(self.p-1))
        
        # #16/3/21
        # self.a = 1
        # # for i in range(2,1000):
        # #     if((i**self.p)%self.q == 1):
        # #         self.a = i
        # #         break
        
        self.d = randint(2,self.q-1)
        self.e_0 = self.getPrimitiveRoot(self.p)
        self.e_1 = PowNMod(self.e_0,((self.p-1)//self.q),self.p)
        self.e_2 = PowNMod(self.e_1,self.d,self.p)
        print(f"Global values are p={self.p} q={self.q} e_1 ={self.e_1} ,e_2 ={self.e_2},d ={self.d}")

    def getPrimitiveRoot(self,p,accuracy_factor=4):
        #more accuracy_factor, more loop iterations
        factors = self.p_numbers.getPrimeFactors(p-1)
        p_root = 0
        for _ in range(10**accuracy_factor):
            _random = randint(2, p-1)
            fact_length = len(factors)
            for i in factors:
                if PowNMod(_random, (p-1)//i, p) != 1:
                    fact_length -= 1
                else:
                    break
            if fact_length == 0:
                p_root = _random
        return p_root

    def hash(self,M):
        return M

    def sign(self,M):
        #getting r
        self.r = randint(1,self.q-1)
        self.euclidean_exteded = EuclidianExtended()
        while self.euclidean_exteded.GetGcd(self.r,self.q) != 1:
            self.r = randint(1,self.q-1)
        print("r=",self.r)
        self.r_inv = self.euclidean_exteded.GetInv(self.r,self.q)

        s_1 = (PowNMod(self.e_1,self.r,self.p))%self.q
        s_2 = ( (self.hash(M)+ self.d * s_1)*self.r_inv )%self.q
        if self.euclidean_exteded.GetGcd(s_2,self.q) != 1:
            print(M,"s_2 is not invertible")
        return (s_1,s_2)

    def is_valid(self,M,s_1,s_2):
        t_2 = s_1
        s_2_inv = self.euclidean_exteded.GetInv(s_2,self.q)
        e_1_rt = (self.hash(M) * s_2_inv)%self.q # the value raise to e1
        e_2_rt = (s_1* s_2_inv)%self.q # the value raise to e2
        t_1 = ((( PowNMod(self.e_1,(e_1_rt),self.p) )*( PowNMod(self.e_2,e_2_rt,self.p) ))%self.p)%self.q
        
        if t_1 == t_2:
            return True
        else:
            return False

    @staticmethod
    def test():
        #case 1 with prime of 7 decimal digit
        print("#Case 1 \nUsing prime of 7 decimal digit")
        dss_e_s = DSS_elgamal_schnorr(7)
        M = int(input("Please enter Plain Text: "))
        s_1,s_2 = dss_e_s.sign(M)
        print("s_1:",s_1,"s_2:",s_2)
        if(dss_e_s.is_valid(M,s_1,s_2)):
            print("Signature is valid")
        else:
            print("Invalid signature")
        
        #case 1 with prime of 7 decimal digit
        print("_"*10)
        print("\n#Case 2\nUsing prime of 14 decimal digit")
        dss_e_s = DSS_elgamal_schnorr(14)
        M = int(input("Please enter Plain Text: "))
        s_1,s_2 = dss_e_s.sign(M)
        print("s_1:",s_1,"s_2:",s_2)
        if(dss_e_s.is_valid(M,s_1,s_2)):
            print("Signature is valid")
        else:
            print("Invalid signature")
        


if __name__ == "__main__":
    DSS_elgamal_schnorr.test()