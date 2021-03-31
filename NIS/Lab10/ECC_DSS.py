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
        delta_x=p_2[0]-p_1[0]
        
        if( p_1[0]!=p_2[0] and p_1[1]!=p_2[1] and EE.GetGcd(abs(delta_x),prime) == 1 ):
            
            if delta_x>0:
                return (p_2[1]-p_1[1])*EE.GetInv(delta_x,prime)%prime
            else:
                return (p_1[1]-p_2[1])*EE.GetInv(-1*delta_x,prime)%prime
        elif(p_1[0]==p_2[0] and p_1[1]==-p_2[1]):
            return float("inf")
        else:
            numerator = (3*p_1[0]*p_1[0] + self.a )
            denomInverse = EE.GetInv(2*p_1[1],prime)
            #print("in getSlope else: ",( numerator*denomInverse )%prime)
            return ( numerator*denomInverse )%prime

    def get_order(self):
        return self.p
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
        scalar = int(scalar)
        if(scalar <= 1):
            return self
        if(scalar & 1 == 1):
            #odd
            res1 = self.multiplyScalar((scalar-1)//2)
            res2 = self.multiplyScalar( (scalar-1)//2 + 1)
            res = res1 + res2
            # print("Multiplying with odd scalar",scalar,"->",(scalar-1)//2,res1,(scalar-1)//2+1,res2)
            # print(res)
            return res
        else:
            
            res = self.multiplyScalar(scalar//2) + self.multiplyScalar(scalar//2)
            # print("Multiplying with even scalar",scalar,"->",(scalar)//2,(scalar)//2)
            # print(res)
            return res
    
    # def multiplyScalar_loop(self,scalar):
    #     point = ECPoint(self.x,self.y,self.ECurve.a,self.ECurve.b,self.ECurve.p)
    #     for i in range(1,scalar):
    #         point = point+self
    #         print(i,point)
    #     return point


    def __str__(self):
        return "({},{}) w.r.t. EC_{}({},{})".format(self.x,self.y,self.ECurve.p,self.ECurve.a,self.ECurve.b)
    @staticmethod
    def test():
        # print("\n####################")
        # print("Testing Elliptic Curve Point addition and scalar multiplication")
        # a=2
        # b=3
        # p=13
        # p_1 = ECPoint(4,2,a,b,p)
        # p_2 = ECPoint(10,6,a,b,p)
        # print(p_1)
        # print(p_2)
        # print("Addition of p_1 and p_2 ",p_1+p_2)
        # print("scalar Multiplication p_1*2 := ",p_1.multiplyScalar(2))

        #case 2
        a=2
        b=2
        p=17
        p_1 = ECPoint(7,6,a,b,p)
        p_2 = ECPoint(5,16,a,b,p)
        # print(p_1.ECurve.getPoints())
        # d=3
        # e_2 = p_1.multiplyScalar(d)
        # print(p_1)
        # print("p1*d",e_2)
        
class ECC_DSS:
    def __init__(self,a,b,p):
        #private Key
        self.d = randint(2,p-2)
        #public key
        self.ECurve = EllipticCurve(a,b,p)
        self.e_1 = self.ECurve.getRandomPoint()
        self.e_2 = self.e_1.multiplyScalar(self.d)    
        self.q = self.ECurve.get_order()
        self.testing = False
        self.r = 1

    def set_e_1(self,x,y):
        self.e_1 = ECPoint(x,y,self.ECurve.a,self.ECurve.b,self.ECurve.p)
        self.e_2 = self.e_1.multiplyScalar(self.d)    

    def sign(self,M):
        
        if(self.testing):
            r=self.r
        else:
            r = randint(1,self.q-2) #secret random number
        ee = EuclidianExtended()
        r_inv = ee.GetInv(r,self.q)
        point1 = self.e_1.multiplyScalar(r)
        s_1 = point1.x % self.q
        s_2 = ( (self.hash(M)+self.d*s_1)*r_inv )%self.q
        return (s_1,s_2)
    def hash(self,M):
        return M

    def is_valid(self,M,s_1,s_2):
        validity = False
        ee = EuclidianExtended()
        s_2_inv = ee.GetInv(s_2,self.q)
        print("s2_inv",s_2_inv)
        t_1 = (self.hash(M)*s_2_inv)%self.q
        t_2 = (s_2_inv*s_1)%self.q
        print("t_1,t_2",t_1,t_2)
        third_point = self.e_1.multiplyScalar(t_1) + self.e_2.multiplyScalar(t_2)
        if third_point.x== s_1%self.q :
            validity = True   
        return validity

    @staticmethod
    def test():
        #case 1
        # a,b,p=2,3,191
        # ecc_dss = ECC_DSS(a,b,p)
        # M=5
        # s_1,s_2=ecc_dss.sign(M)
        # print(ecc_dss.is_valid(M,s_1,s_2))
        #case 2 from notes
        a,b,p=2,2,17
        ecc_dss = ECC_DSS(a,b,p)
        ecc_dss.set_e_1(16,13)
        M=45
        s_1,s_2=ecc_dss.sign(M)
        print("s1:",s_1,",s2:",s_2)
        if(ecc_dss.is_valid(M,s_1,s_2)):
            print("Message Valid")
        

if __name__ == "__main__":
    #ECPoint.test()
    ECC_DSS.test()