# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 19:27:34 2020

@author: RAHIL
"""

def getKey(LangX_Probability,LangY,maxChar=26):
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
    
    LangY = [c for c in LangY]
    LangY.sort()
    print(LangY)
    setLangY = set(LangY)
    n = len(LangY)
    LangY_Probability = [LangY.count(c)/n for c in setLangY]
    print(LangY_Probability)
    
    #for i in range(maxChar):
        
getKey([0.8,0.1], "LangYafssdfzxcvbnmasdfghjklqwertyuiop")