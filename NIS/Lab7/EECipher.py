from EllipticCurve import EllipticCurve
from EllipticCurve import EllipticCurve
from math import pow
class EECPoint(EllipticCurve):
    def __init__(self,x,y,a,b,p):
        self.x=x
        self.y=y
        self.EEC = EllipticCurve(a,b,p)

    def __add__(self,p_2):
        slope = self.EEC.getSlope((self.x,self.y),(p_2.x,p_2.y),self.EEC.p)
        print("slope:",slope)
        x3 = (pow(slope,2) - self.x - p_2.x)%self.EEC.p
        y3 = (slope*(self.x-x3) - self.y)%self.EEC.p
        return EECPoint(x3,y3,self.EEC.a,self.EEC.b,self.EEC.p)
        
    def multiplyScalar(self,scalar):
        print(scalar)
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
        return "({},{}) EE_{}({},{})".format(self.x,self.y,self.EEC.p,self.EEC.a,self.EEC.b)
    def test(self):
        p_2 = self.EEC.getRandomPoint()
        print(self)
        print(p_2)
        print(self + p_2)

if __name__ == "__main__":
    a=2
    b=3
    p=13
    p_1 = EECPoint(4,2,a,b,p)
    p_2 = EECPoint(10,6,a,b,p)
    print(p_1)
    print(p_2)
    print(p_1+p_2)
    print(p_1.multiplyScalar(2))