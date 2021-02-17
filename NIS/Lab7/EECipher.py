from Utilities import EuclidianExtended, PowNMod
from math import ceil,sqrt
from random import randint
from math import pow

class EllipticCurve:
    def __init__(self,a,b,p):
        self.a = a
        self.b = b
        self.p = p
        self.isParametersValid() 
        self.point_list = []
    def isParametersValid(self):
        #checks validity of a and b 
        if ( 4*self.a**3+27*self.b**2 == 0):
            print("inappropriate combination of a and b please change it")
            return False
        else:
            #print("Valid combination of a and b ")
            return True
    def getPoints(self):
        if(self.isParametersValid()):
            x=0
            point_list = []
            while x < self.p:
                w = (x**3 + self.a*x + self.b)%self.p
                if( PowNMod(w,(self.p-1)//2,self.p) == 1 ):
                    # w is a QR
                    root = sqrt(w)
                    while ceil(root) != root:
                        w+=self.p
                        root = sqrt(w)
                    point_list.append((x,int(root%self.p)))
                    point_list.append((x,int((-root)%self.p)))
                if(PowNMod(w,(self.p-1)//2,self.p) == self.p-1 ):
                    #print("No solution Possible for x = {0}".format(x))
                    pass
                x+=1
            self.point_list = point_list
            return point_list
        else:
            return []
    
    def getRandomPoint(self):
        if(len(self.point_list) == 0):
            self.getPoints()
        index = randint(0,len(self.point_list)-1)
        point = self.point_list[index]
        eCPoint = ECPoint(point[0],point[1],self.a,self.b,self.p)
        return eCPoint

    def getSlope(self,p_1,p_2,prime):
        EE = EuclidianExtended()
        if( p_1[0]!=p_2[0] and p_1[1]!=p_2[1] ):
            delta_x=p_2[0]-p_1[0]
            return (p_2[1]-p_1[1])*EE.GetInv(delta_x,prime)%prime
        elif(p_1[0]==p_2[0] and p_1[1]==-p_2[1]):
            return float("inf")
        else:
            numerator = (3*p_1[0]*p_1[0] + self.a )
            denomInverse = EE.GetInv(2*p_1[1],prime)
            #print("in getSlope else: ",( numerator*denomInverse )%prime)
            return ( numerator*denomInverse )%prime
    def test(self):
        a=2
        b=3
        p=67
        ec = EllipticCurve(a,b,p)
        print(ec.getPoints())
        a=1
        b=1
        p=13
        ec = EllipticCurve(a,b,p)
        print(ec.getPoints())
        print(ec.getSlope((35,66),(42,26),67))
        print(ec.getSlope((35,66),(35,66),67))
    

class ECPoint:
    def __init__(self,x,y,a,b,p):
        self.x=x
        self.y=y
        self.ECurve = EllipticCurve(a,b,p)

    def __add__(self,p_2):
        slope = self.ECurve.getSlope((self.x,self.y),(p_2.x,p_2.y),self.ECurve.p)
        #print("slope:",slope)
        x3 = (pow(slope,2) - self.x - p_2.x)%self.ECurve.p
        y3 = (slope*(self.x-x3) - self.y)%self.ECurve.p
        return ECPoint(x3,y3,self.ECurve.a,self.ECurve.b,self.ECurve.p)
        
    def __sub__(self,p_2):
        p_2.y=-p_2.y
        return self + p_2

    def multiplyScalar(self,scalar):
        #print(scalar)
        if(scalar <= 1):
            return self
        if(scalar & 1 == 1):
            #odd
            #print(self.multiplyScalar((scalar-1)//2) , self.multiplyScalar( (scalar-1)//2 + 1))
            return self.multiplyScalar((scalar-1)//2) + self.multiplyScalar( (scalar-1)//2 + 1)
        else:
            #print(self.multiplyScalar((scalar)//2) , self.multiplyScalar( (scalar)//2 + 1))
            return self.multiplyScalar(scalar//2) + self.multiplyScalar(scalar//2)

    def __str__(self):
        return "({},{}) w.r.t. EC_{}({},{})".format(self.x,self.y,self.ECurve.p,self.ECurve.a,self.ECurve.b)
    @staticmethod
    def test():
        print("\n####################")
        print("Testing Elliptic Curve Point addition and scalar multiplication")
        a=2
        b=3
        p=13
        p_1 = ECPoint(4,2,a,b,p)
        p_2 = ECPoint(10,6,a,b,p)
        print(p_1)
        print(p_2)
        print("Addition of p_1 and p_2 ",p_1+p_2)
        print("scalar Multiplication p_1*2 := ",p_1.multiplyScalar(2))

class ECCipher:
    def __init__(self,a,b,p):
        #private Key
        self.d = randint(2,p-2)
        #public key
        self.ECurve = EllipticCurve(a,b,p)
        self.e_1 = self.ECurve.getRandomPoint()
        self.e_2 = self.e_1.multiplyScalar(self.d)    
        self.testing = False
        self.r = 1

    def encrypt(self,M):
        
        if(self.testing):
            r=self.r
        else:
            r = randint(1,self.ECurve.p-2)
        c_1 = self.e_1.multiplyScalar(r)
        c_2 = M + self.e_2.multiplyScalar(r)
        return [c_1,c_2]

    def decrypt(self,c_1,c_2):
        M = c_2 - c_1.multiplyScalar(self.d)
        return M

    def test(self):
        a,b,p=1,1,13
        #self = ECCipher(a,b,p)
        self.e_1 = ECPoint(1,4,a,b,p)
        self.d = 4
        self.e_2 = self.e_1.multiplyScalar(self.d)
        self.testing = True
        print("\n##############\nTesting ECCipher")
        print("e1: ",self.e_1,"\ne2: ",self.e_2)
        print("d = {0}".format(self.d))
        plainPoint = ECPoint(12,5,a,b,p)
        print("plain point: ",plainPoint)
        cipherPoints = self.encrypt(plainPoint)
        print("ciphered point: ",cipherPoints[0],cipherPoints[1])
        decipheredPoint = self.decrypt(cipherPoints[0],cipherPoints[1])
        print("deciphered point",decipheredPoint,"\n")
if __name__ == "__main__":
    ECPoint.test()
    ECCipher(1,1,13).test()