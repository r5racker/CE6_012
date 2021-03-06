from KasaskiTest import KasaskiTest
from AdditiveCipher import AdditiveCipher


class VigenereCipher:
    def __init__(self, keyString, base=ord("a")):
        self.base = base
        self.SecretKey = [ord(ch)-base for ch in keyString]

    def encrypt(self, plainText):
        m = len(self.SecretKey)
        plainText = plainText.lower()
        cipher = []
        base = ord('a')
        for i in range(len(plainText)):
            delta = (ord(plainText[i]) - self.base +
                     self.SecretKey[i % m]) % 26
            cipher.append(chr(base + delta))
        return ''.join(cipher)

    def decrypt(self, cipherText):
        m = len(self.SecretKey)
        plainText = []
        for i in range(len(cipherText)):
            delta = (ord(cipherText[i]) - self.base -
                     self.SecretKey[i % m]) % 26
            plainText.append(chr(self.base + delta))
        return ''.join(plainText)

    def getKeysFromCipher(self, cipherText, length):
        secretKeysRetrived = []
        Y_parts = []
        AC = AdditiveCipher()
        for i in range(length):
            part = cipherText[i::length]
            Y_parts.append(part)
            tempKey = AC.getKeyFromCipher(
                AC.english_probability, Y_parts[i], 26)

            secretKeysRetrived.append(chr(self.base + tempKey))
        secretKeysRetrived = "".join(secretKeysRetrived)
        return secretKeysRetrived

    def analyse(self, cipherText):
        KT = KasaskiTest()
        m = KT.findLength(cipherText, 25)
        print("M := ", m)
        keysRetrived = self.getKeysFromCipher(cipherText, m)
        print("Keys : ", keysRetrived)


option = input("Do you want to try it yourself or see ready example? Y/N : ")
if option == "N":
    plainText = "TheHitchhikersGuidetotheGalaxyisthefirstofsixbooksintheHitchhikersGuidetotheGalaxycomedysciencefictiontrilogybyDouglasAdamsThenovelisanadaptationofthefirstfourpartsofAdamssradioseriesofthesamenameThenovelwasfirstpublishedinLondononOctoberItsoldcopiesinthefirstthreemonths"
    key = "pascal"
    VC = VigenereCipher(key, ord("a"))
    cipher = VC.encrypt(plainText)
    print("Plain text : ", plainText)
    print("Key : ", key)
    print("cipher : ", cipher)
    VC.analyse(cipher)
else:
    plainText = input("enter plain text string : ")
    key = input("enter key string : ")
    VC = VigenereCipher(key, ord("a"))
    cipher = VC.encrypt(plainText)
    print("Plain text : ", plainText)
    print("Key : ", key)
    print("cipher : ", cipher)
    VC.analyse(cipher)
