from Utilities import EuclidianExtended, PowNMod, PrimeNumbers
class PrimitiveRoots:
    def getPrimitiveRoots(self,p):
        EE = EuclidianExtended()
        #phi_p = self.phi(p)
        phi_p = 0
        empty_set = set()
        sub_group_orders = []
        for a in range(p):
            if(EE.GetGcd(a,p) == 1):
                #calculating co-primes
                phi_p += 1
                #print(f"a={a}")
                temp_set = set()
                for i in range(p):
                    temp = PowNMod(a,i,p)
                    #print(f"\ttemp={temp}")
                    if temp_set.intersection({temp}) ==  empty_set:
                        temp_set.add(temp)
                    else:
                        break
                sub_group_orders.append((a,len(temp_set)))
            else:
                continue
        primitive_roots = [a for (a,o) in sub_group_orders if(o == phi_p) ]
        coprime_list = [a for (a,o) in sub_group_orders]
        return primitive_roots,coprime_list
    def test(self):
        p = 50
        print(f"primitive roots of z_{p} are :")
        primitive ,_ = self.getPrimitiveRoots(p)
        print(primitive)
if __name__ == "__main__":
    PR = PrimitiveRoots()
    PR.test()