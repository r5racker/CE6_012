# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 19:27:34 2020

@author: RAHIL
"""
from AdditiveCipher import AdditiveCription as AC

'''
            # Frequencies

            A :  8.55        K :  0.81        U :  2.68
            B :  1.60        L :  4.21        V :  1.06
            C :  3.16        M :  2.53        W :  1.83
            D :  3.87        N :  7.17        X :  0.19
            E : 12.10        O :  7.47        Y :  1.72
            F :  2.18        P :  2.07        Z :  0.11
            G :  2.09        Q :  0.10
            H :  4.96        R :  6.33
            I :  7.33        S :  6.73
            J :  0.22        T :  8.94
            '''


class AdditiveCryptAnalysis:
    def __init__(self):
        self.alphabets = "abcdefghijklmnopqrstuvwxyz"
        self.english_probability = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
                                    0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
                                    0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
                                    0.00978, 0.02360, 0.00150, 0.01974, 0.00074]

    def getKey(self, LangX_Probability, LangY, maxChar=26):
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
        print("Extracting Key from cipher\n____________")
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
        print("MIC : ", max_MI)
        key = MI_buffer.index(max_MI)
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

    def test(self):

        print("\n-----Testing Crypt Analysis for Additive additive cipher -----\n")
        plain = """TheHitchhikersGuidetotheGalaxyisthefirstofsixbooksintheHitchhikersGuidetotheGalaxycomedysciencefictiontrilogybyDouglasAdamsThenovelisanadaptationofthefirstfourpartsofAdamssradioseriesofthesamenameThenovelwasfirstpublishedinLondononOctoberItsoldcopiesinthefirstthreemonths"""
        print("Plain : ", plain)
        AKey = 10
        cipher = AC(AKey).encrypt(plain)
        print("encrypting using key : ", AKey)
        print("cipher :")
        print("_________________________")
        print("Performing Analysis")
        key = self.getKey(self.english_probability, cipher.lower())
        print("Key extracted : ", key, "\n")


CAAdditive = AdditiveCryptAnalysis()
CAAdditive.test()
