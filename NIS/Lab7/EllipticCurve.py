from Utilities import EuclidianExtended, PowNMod
from math import ceil,sqrt
from random import randint
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
            print("Valid combination of a and b ")
            return True
    def getPoints(self):
        if(self.isParametersValid()):
            x=0
            point_list = []
            while x < p:
                w = (x**3 + a*x + b)%self.p
                if( PowNMod(w,(self.p-1)//2,self.p) == 1 ):
                    # w is a QR
                    root = sqrt(w)
                    while ceil(root) != root:
                        w+=self.p
                        root = sqrt(w)
                    point_list.append((x,int(root%self.p)))
                    point_list.append((x,int((-root)%self.p)))
                if(PowNMod(w,(self.p-1)//2,self.p) == p-1 ):
                    print("No solution Possible for x = {0}".format(x))
                x+=1
            self.point_list = point_list
            return point_list
        else:
            return []
    
    def getRandomPoint(self):
        if(self.point_list == []):
            self.getPoints()
        index = randint(0,len(self.point_list))
        return self.point_list[index]

    def getSlope(self,p_1,p_2,prime):
        EE = EuclidianExtended()
        if( p_1[0]!=p_2[0] and p_1[1]!=p_2[1] ):
            delta_x=p_2[0]-p_1[0]
            return (p_2[1]-p_1[1])*EE.GetInv(delta_x,prime)%prime
        elif(p_1[0]==p_2[0] or p_1[1]==-p_2[1]):
            return float("inf")
        else:
            numerator = (3*p_1[0]*p_1[0] + self.a )
            denomInverse = EE.GetInv(2*p_1[1],prime)
            return ( numerator*denomInverse )%prime

if __name__ == "__main__":
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
