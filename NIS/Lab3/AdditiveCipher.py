# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 15:31:17 2020

@author: RAHIL
"""


class AdditiveCipher:

    def __init__(self, secretKey=0):
        self.secretKey = secretKey
        self.alphabets = "abcdefghijklmnopqrstuvwxyz"
        self.english_probability = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
                                    0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
                                    0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
                                    0.00978, 0.02360, 0.00150, 0.01974, 0.00074]
        self.icThreshold = 0.01
        self.base = ord("a")

    def encrypt(self, plainText):
        plainText = plainText.lower()
        cript = []
        base = ord('a')
        for c in plainText:
            delta = (ord(c) - ord('a') + self.secretKey) % 26
            cript.append(chr(base + delta))
        return ''.join(cript)

    def encryptWithKey(self, plainText, key):
        plainText = plainText.lower()
        cript = []
        base = ord('a')
        for c in plainText:
            delta = (ord(c) - base + key) % 26
            cript.append(chr(base + delta))
        return ''.join(cript)

    def decrypt(self, cipher):
        plainText = []
        base = ord('a')
        for c in cipher:
            delta = (ord(c) - base - self.secretKey) % 26
            plainText.append(chr(base + delta))
        return ''.join(plainText)

    def decryptByKey(self, cipher, key):
        plainText = []
        base = ord('a')
        for c in cipher:
            delta = (ord(c) - ord('a') - key) % 26
            plainText.append(chr(base + delta))
        return ''.join(plainText)

    def analyse(self, cipher):
        print("Analysing cription for \""+cipher+"\"")
        for i in range(26):
            print("#"+str(i), " ", self.decryptByKey(cipher, i))

    def getKeyFromCipher(self, LangX_Probability, LangY, maxChar=26):
        '''
        Parameters
        ----------
        LangX_Probability : [P0,P1, ... P_(maxChar-1) ]
            List of Probability of each characters in languageX.
        LangY : string
            cypher string of languageY.
        maxChar : Int, optional
            maximum number of character types in language X. The default is 26.

        Returns key : Int
            key that has been used in encrypting languageX to LanguageY
        -------
        '''
        print("____________\nExtracting Key from cipher")
        LangY = [c for c in LangY]
        LangY_Probability = self.getProb(LangY)
        MI_buffer = []
        for countI in range(len(LangX_Probability)):
            # summation of Pi*Pi' for i ==> [0,25]
            MI = sum([LangX_Probability[countJ]*LangY_Probability[countJ]
                      for countJ in range(len(LangX_Probability))])
            MI_buffer.append(MI)
            LangY_Probability.append(LangY_Probability.pop(0))
        max_MI = max(MI_buffer)
        key = MI_buffer.index(max_MI)
        print("MIC : ", max_MI, "Key", chr(self.base + key))
        return key

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

    def testAnalysis(self):

        print("\n-----Testing Crypt Analysis for Additive additive cipher -----\n")
        plain = """TheHitchhikersGuidetotheGalaxyisthefirstofsixbooksintheHitchhikersGuidetotheGalaxycomedysciencefictiontrilogybyDouglasAdamsThenovelisanadaptationofthefirstfourpartsofAdamssradioseriesofthesamenameThenovelwasfirstpublishedinLondononOctoberItsoldcopiesinthefirstthreemonths"""
        print("Plain : ", plain)
        AKey = 10
        cipher = self.encryptWithKey(plain, AKey)
        print("encrypting using key : ", AKey)
        print("cipher :")
        print("_________________________")
        print("Performing Analysis")
        key = self.getKey(self.english_probability, cipher.lower())
        print("Key extracted : ", key, "\n")


if(__name__ == "__main__"):
    testKey = int(input("enter Key for encryption (0-25) :"))
    testText = input("Plain Text: ")
    Cripter = AdditiveCipher(testKey)
    cipher = Cripter.encrypt(testText)
    print("string :", testText)
    print("key :", testKey)
    print("encrypted", cipher)
    print("decripted : ", Cripter.decrypt(cipher))
    Cripter.analyse(cipher)
