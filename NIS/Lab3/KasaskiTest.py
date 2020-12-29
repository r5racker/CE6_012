class KasaskiTest:
    def __init__(self):
        self.englishIC = 0.065
        self.alphabets = "abcdefghijklmnopqrstuvwxyz"
        self.icThreshold = 0.01

    def findLength(self, cipherText, max_length):
        for i in range(1, max_length):
            res = self.TestLength(cipherText, i)
            if res:
                return i

    def TestLength(self, cipherText, length):
        # partition
        Y_parts = []
        Y_ICs = []
        AllEqual = True
        comparisonString = ""
        for i in range(length):
            part = cipherText[i::length]
            Y_parts.append(part)
            tempIC = self.calculateIC(part)
            if abs(tempIC - self.englishIC) < self.icThreshold:
                comparisonString += "1"
            else:
                comparisonString += "0"
                AllEqual = False
            Y_ICs.append(tempIC)
        avgIc = sum(Y_ICs)/len(Y_ICs)
        # print(Y_parts)
        # print(Y_ICs)
        #print("__________", length, avgIc, comparisonString)

        # checking number of near ICs and deciding over majority
        majorityRation = 0.6  # ration to consider whether match is valid or not
        if(comparisonString.count("1")/len(comparisonString) > majorityRation):
            AllEqual = True
        #

        if abs(self.englishIC - avgIc) < self.icThreshold and AllEqual:
            return True
        else:
            return False

    def calculateIC(self, Lang):
        n = len(Lang)
        langFreq = self.getFreq(Lang)
        #langProb = self.getProb(Lang)
        #Ic = sum([p*p for p in langProb])
        Ic = sum([f*(f-1)/(n*n) for f in langFreq])
        return Ic

    def getProb(self, LangYList):
        '''
        Parameters
        ----------
        LangYList : List
            list of characters in unknown language.

        Returns
        -------
        ProbList : List
            Probability of characters in language.

        '''

        alphabetsList = [c for c in self.alphabets]
        n = len(LangYList)
        # print(LangYList, n)
        ProbList = [LangYList.count(c)/n for c in alphabetsList]
        return ProbList

    def getFreq(self, LangYList):
        '''
        Parameters
        ----------
        LangYList : List
            list of characters in unknown language.

        Returns
        -------
        ProbList : List
            Probability of characters in language.

        '''

        alphabetsList = [c for c in self.alphabets]
        n = len(LangYList)
        # print(LangYList, n)
        freqList = [LangYList.count(c) for c in alphabetsList]
        return freqList

    def test(self):
        key = "pascal"
        cipher = "ihwjierhzkkpgsywiottgvhpvadcxjxsljeqxrkvoqhipdozzsaptsthavcswicgrdvuafeedtzgglaapaczbevasnxefeeqxclkoyiranornbqfofvlsuaopmkvhpconglthafcdletsvizcoxvhpuijutqdujracisghaopmkurlsiguecxekqfewekcmpcaegtstngxewlakhichthwbwxszgdtclgpdzcofqcedbwtiehodfczeiwuiyihwhichtljrptmgptsh"
        length = self.findLength(cipher, 26)
        print("key was ", key)
        print("cipher was : ", cipher)
        print("predicted length : ", length)


if __name__ == "__main__":
    KT = KasaskiTest()
    KT.test()
