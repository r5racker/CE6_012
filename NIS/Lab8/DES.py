from math import sqrt 
import numpy as np
import copy

class BitBlock:
    def __init__(self,hex_data):
        '''
        hex_data : hexa decimal data
        '''
        self.bit_string = self.get_bitstring_from_hex(hex_data)
        #debug
        #print("BitBlock(): ",self.bit_string)
        self.size = len(self.bit_string)

    def set_bit_string(self,bit_string):
        self.bit_string = bit_string
        self.size = len(self.bit_string)
        #debug
        #print("bit_string",bit_string)
        return self
    def set_bit_string_from_decimal(self,decimal_string):
        bit_s= self.get_binary_from_decimal(decimal_string)
        return self.set_bit_string(bit_s)

    def get_bit(self,index):
        return self.bit_string[index]

    def get_bit_sequence(self,start_index,end_index):
        '''Returns bits in range start_index to end_index including start index only'''
        return self.bit_string[start_index:end_index]

    def get_hex_string(self):
        return self.get_hex_from_bit_string(self.bit_string)
    @staticmethod
    def get_bitstring_from_hex(hex_data):
        binString = ''
        for hexDigit in hex_data:
            binDigitString = bin(int(hexDigit, 16))[2:]
            binString += binDigitString.zfill(4)
        return binString
    @staticmethod
    def get_hex_from_bit_string(bin_string):
        return hex(int(bin_string,2)).replace("0x","").upper()
    @staticmethod
    def get_decimal_from_binary(binary_string):
        return int(str(binary_string),2)
    @staticmethod
    def get_binary_from_decimal(decimal_num):  
        binary_string = bin(decimal_num).replace("0b", "") 
        if(len(binary_string)%4 != 0): 
            hexPartitions = len(binary_string) // 4
            binary_string = binary_string.zfill(4 * (hexPartitions + 1))
        return binary_string

    def perform_permutation(self,permutation_table,is_table_sequence_from_zero=False,is_expansion=False):
        permuted_string = ""
        if self.size >= len(permutation_table) or is_expansion:
            for index in permutation_table:
                if(is_table_sequence_from_zero):
                    permuted_string += self.bit_string[index]
                else:
                    permuted_string += self.bit_string[index-1]
        else:
            #debug
            #print("Permutation out of reach,size of current block is :",self.size," and length of permituation table is :",len(permutation_table))
            raise ValueError("Permutation out of reach, Please change the parameter flag if you are trying for expansion permutation; size of current block is :",self.size," and length of permituation table is :",len(permutation_table))
        return BitBlock("").set_bit_string(permuted_string)
        
    def split(self,fragmentSize):
        splited_string = [self.bit_string[0+i:fragmentSize+i] for i in range(0, len(self.bit_string), fragmentSize)]
        return [BitBlock("").set_bit_string(st) for st in splited_string]
        
    def splitHalf(self):
        halfs = self.split(self.size//2)
        return halfs[0],halfs[1]

    def left_shift(self,n):
        self.bit_string = self.bit_string[n:]+self.bit_string[:n]
    
    def XOR(self,bit_block_2):
        xored_string = ""
        if self.size == bit_block_2.size:
            for i in range(self.size):
                if self.bit_string[i]==bit_block_2.bit_string[i]:
                    xored_string+= "0"
                else:
                    xored_string+= "1"

        #debug
        #print("XOR : ",xored_string)

        return BitBlock("").set_bit_string(xored_string)
    
    def __add__(self,bit_block_2):
        return BitBlock("").set_bit_string(self.bit_string+bit_block_2.bit_string)

    @staticmethod
    def test():
        initial_perm = [58, 50, 42, 34, 26, 18, 10, 2,
                60, 52, 44, 36, 28, 20, 12, 4,
                62, 54, 46, 38, 30, 22, 14, 6,
                64, 56, 48, 40, 32, 24, 16, 8,
                57, 49, 41, 33, 25, 17, 9, 1,
                59, 51, 43, 35, 27, 19, 11, 3,
                61, 53, 45, 37, 29, 21, 13, 5,
                63, 55, 47, 39, 31, 23, 15, 7]
        data = BitBlock("0123456789ABCDEF")
        print(data.bit_string)
        #print(initial_perm)
        print(data.perform_permutation(initial_perm,is_table_sequence_from_zero=False).bit_string)
        print(data.splitHalf())
        
class KeyBlock(BitBlock):
    def __init__(self, hex_key_string):
        super().__init__(hex_key_string)
        self.original_hex_key_string = hex_key_string
        self.initial_key_compression() #converts 64bit key to 56bit key
        self.LK,self.RK = self.splitHalf()
        
        self.round_key_stack = [] # stack of keys generated for each round[0-15]
        self.round_count=16
        self.round_key_shift_count = [1, 1, 2, 2,
                                    2, 2, 2, 2,
                                    1, 2, 2, 2,
                                    2, 2, 2, 1 ]

    def set_lk_rk(self):
        self.LK,self.RK = self.splitHalf() # 28 bit key fragment each

    def set_bit_string(self, bit_string):
        super().set_bit_string(bit_string)
        self.set_lk_rk()

    def initial_key_compression(self):
        #performs compression of key from 64bits to 56bits by discarding every 8th bits
        # initial_compression_permutation_table = [
        #     1,2,3,4,5,6,7,9,10,11,12,13,14,15,
        #     17,18,19,20,21,22,23,25,26,27,28,29,30,31,
        #     33,34,35,36,37,38,39,41,42,43,44,45,46,47,
        #     49,50,51,52,53,54,55,57,58,59,60,61,62,63
        # ]

        initial_compression_permutation_table = [57, 49, 41, 33, 25, 17, 9,  
        1, 58, 50, 42, 34, 26, 18,  
        10, 2, 59, 51, 43, 35, 27,  
        19, 11, 3, 60, 52, 44, 36,  
        63, 55, 47, 39, 31, 23, 15,  
        7, 62, 54, 46, 38, 30, 22,  
        14, 6, 61, 53, 45, 37, 29,  
        21, 13, 5, 28, 20, 12, 4 ] 
        print("\n"+"#"*4+"Performing Initial key compression"+"#"*4)
        print("initial key:\t",self.get_hex_string())
        print("size:\t"+str(self.size)+"bits")
        compressed_key = self.perform_permutation(initial_compression_permutation_table,is_table_sequence_from_zero=False)
        
        print("compressed Key :",compressed_key.get_hex_string())
        self.set_bit_string(compressed_key.bit_string)

    def compression_permutation(self):
        '''
        Performs compression for each key generation step by converting 56bit key format to 48bits 
        returns transformedKey(BitBlock): 48 bits
        '''
        key_compression_permitation_table = [14, 17, 11, 24, 1, 5,  
            3, 28, 15, 6, 21, 10,  
            23, 19, 12, 4, 26, 8,  
            16, 7, 27, 20, 13, 2,  
            41, 52, 31, 37, 47, 55,  
            30, 40, 51, 45, 33, 48,  
            44, 49, 39, 56, 34, 53,  
            46, 42, 50, 36, 29, 32 ]
        self.bit_string = self.LK.bit_string + self.RK.bit_string
        return self.perform_permutation(key_compression_permitation_table,is_table_sequence_from_zero=False)
    
    def generate_keys(self) :
        self.round_key_stack= []
        #debug
        print("Generating Round Keys")
        print("initial Key:",self.get_hex_string())
        for i in range(self.round_count):
            # print("debug in generate_keys:",i," shift:",self.round_key_shift_count[i])
            # print("LK RK",self.LK.bit_string,self.RK.bit_string)

            self.LK.left_shift(self.round_key_shift_count[i])
            self.RK.left_shift(self.round_key_shift_count[i])
            
            current_round_key = self.compression_permutation()
            self.round_key_stack.append(current_round_key)
    
    def get_round_key(self,round_number):
        '''
            Parameter round_number(int): the round number for which key is requested in range [1 upto round_count] 
            Returns 48 bit ready round key for requested round
        '''
        if len(self.round_key_stack) <= 0:
            self.generate_keys()

        if(len(self.round_key_stack)>=round_number):
            return self.round_key_stack[round_number-1]
        
    @staticmethod
    def test():
        '''
        test_bit_block_1 = BitBlock("0123456789ABCDEF")
        print("",test_bit_block_1.bit_string)

        test_lshift_object = KeyBlock("AABB09182736CCDD")
        test_lshift_object.left_shift(2)
        print("BitString after left shift by 2:\n",test_lshift_object.bit_string)
        #Testing XOR
        test_object_1 = KeyBlock("0123456789ABCDEF")
        test_object_2 = KeyBlock("0123456789ABCDEF")
        print("XOR of same object:\n",test_object_1.XOR(test_object_2).bit_string)
        
        test_roundkeys_object = KeyBlock("AABB09182736CCDD")
        #expected o/p: 11000011110000000011001110100011001111110000110011111010
        
        print("Initial BitString:\n",test_roundkeys_object.bit_string)
        print("round Keys")
        test_roundkeys_object.generate_keys()
        print(test_roundkeys_object.round_key_stack)
        '''
        #expected o/p
        # ['000110010100110011010000011100101101111010001100', '010001010110100001011000000110101011110011001110', 
        # '000001101110110110100100101011001111010110110101', '110110100010110100000011001010110110111011100011', 
        # '011010011010011000101001111111101100100100010011', 
        # '110000011001010010001110100001110100011101011110', '011100001000101011010010110111011011001111000000',
        # '001101001111100000100010111100001100011001101101', '100001001011101101000100011100111101110011001100', 
        # '000000100111011001010111000010001011010110111111', '011011010101010101100000101011110111110010100101', 
        # '110000101100000111101001011010100100101111110011', 
        # '100110011100001100010011100101111100100100011111', '001001010001101110001011110001110001011111010000', 
        # '001100110011000011000101110110011010001101101101', '000110000001110001011101011101011100011001101101']
        # test_roundkeys_object = KeyBlock(BitBlock.get_hex_from_bit_string("1011111100011001111100110001101011111101111000101001111100101010"))
        # print(test_roundkeys_object.get_hex_string())
        # test_roundkeys_object.generate_keys()
        # for k in test_roundkeys_object.round_key_stack:
        #     print(k.bit_string)



class DESCryptography:
    def __init__(self,key_hex):
        '''
        key_hex (KeyBlock): hexadecimal string which represents 64 bits key
        '''
        self.master_key = KeyBlock(key_hex)
    
    def perform_substitution(self,data_block):
        '''
        this is the function for s_box component
        
        Parameters: data_block(BitBlock) 48bits
        
        return substituted_block(BitBlock): block after substitution 32bits
        '''
        sbox_table =  [
            [
                [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
                [ 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
                [ 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
                [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13 ]
            ],
            [
                [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
                [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
                [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
                [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9 ]
            ],
            [
                [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
                [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
                [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
                [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12 ]
            ],
            [
                [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
                [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
                [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
                [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
            ],
            [
                [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
                [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
                [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
                [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3 ]
            ],
            [
                [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
                [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
                [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
                [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
            ],
            [
                [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
                [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
                [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
                [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
            ],
            [
                [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
                [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
                [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
                [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
            ]
        ]

        shrinked_block = BitBlock("")
        sub_blocks = data_block.split(6) # gives list of blocks with size 6 bits, data_block:48bits  ==> 8 elements in list
        for i in range(len(sub_blocks)):
            block = sub_blocks[i]
            row_index = BitBlock.get_decimal_from_binary(block.get_bit(0)+block.get_bit(5))
            col_index = BitBlock.get_decimal_from_binary(block.get_bit_sequence(1,5))
            s_val = sbox_table[i][row_index][col_index] #decimal
            s_val_block = BitBlock("").set_bit_string_from_decimal(s_val)
            shrinked_block += s_val_block
        return shrinked_block #32bits

    def round_function(self,left_block,right_block,round_key):
        #32 -> 48
        expansion_permutation_table = [32, 1 , 2 , 3 , 4 , 5 , 4 , 5,
            6 , 7 , 8 , 9 , 8 , 9 , 10, 11,
            12, 13, 12, 13, 14, 15, 16, 17,
            16, 17, 18, 19, 20, 21, 20, 21,
            22, 23, 24, 25, 24, 25, 26, 27,
            28, 29, 28, 29, 30, 31, 32, 1 ]
        
        #48 -> 32
        end_permutation_table = [ 16,  7, 20, 21,
                        29, 12, 28, 17,
                        1, 15, 23, 26,
                        5, 18, 31, 10,
                        2,  8, 24, 14,
                        32, 27,  3,  9,
                        19, 13, 30,  6,
                        22, 11,  4, 25 ]

        permuted_right_block = right_block.perform_permutation(expansion_permutation_table,is_expansion=True)
        xored_right_block = permuted_right_block.XOR(round_key)
        subsituted_right_block = self.perform_substitution(xored_right_block)
        end_permuted_right_block =subsituted_right_block.perform_permutation(end_permutation_table)#permuted 32 bits
        end_xored_right_block = end_permuted_right_block.XOR(left_block)
        return end_xored_right_block

    def process_fiestal_structure(self,text_block,is_encryption=True):
        initial_permutation_table = [58, 50, 42, 34, 26, 18, 10, 2,
                60, 52, 44, 36, 28, 20, 12, 4,
                62, 54, 46, 38, 30, 22, 14, 6,
                64, 56, 48, 40, 32, 24, 16, 8,
                57, 49, 41, 33, 25, 17, 9, 1,
                59, 51, 43, 35, 27, 19, 11, 3,
                61, 53, 45, 37, 29, 21, 13, 5,
                63, 55, 47, 39, 31, 23, 15, 7]

        final_permutation_table = [ 40, 8, 48, 16, 56, 24, 64, 32,
                39, 7, 47, 15, 55, 23, 63, 31,
                38, 6, 46, 14, 54, 22, 62, 30,
                37, 5, 45, 13, 53, 21, 61, 29,
                36, 4, 44, 12, 52, 20, 60, 28,
                35, 3, 43, 11, 51, 19, 59, 27,
                34, 2, 42, 10, 50, 18, 58, 26,
                33, 1, 41, 9, 49, 17, 57, 25 ]

        permuted_text_block = text_block.perform_permutation(initial_permutation_table)
        #debug
        print("\n"+"#"*10+"Initiating Fiestal Structure"+"#"*10+"\n")
        print("Initially permuted Plain Text")
        print("-"*4+permuted_text_block.get_hex_string()+"\n")
        
        left_block,right_block = permuted_text_block.splitHalf()

        round_start_index =1
        round_end_index = self.master_key.round_count+1
        delta = 1
        if not is_encryption:
            round_start_index = self.master_key.round_count
            round_end_index = 0
            delta = -1
        #debug
        #print("fiestal : start",round_start_index," end:",round_end_index," delta:",delta)
        
        for i in range(round_start_index,round_end_index,delta):
            temp_right_block = copy.deepcopy(right_block)
            current_round_key = self.master_key.get_round_key(i)
            right_block = self.round_function(left_block,right_block,current_round_key)
            left_block = temp_right_block
            
            #debug
            # print("\n#"+str(i-1)+"-round")
            # print("\tright: ",right_block.get_hex_string())
            # print("\t left: ",left_block.get_hex_string())

        #last round needs no swap, so undoing the last swap by swaping once more
        combined_block = right_block + left_block
        
        print("combined data block:\n"+"-"*4+">"+combined_block.get_hex_string())
        final_permuted_block = combined_block.perform_permutation(final_permutation_table)
        #debug
        print("Final Permuted/cipher block:\n"+"-"*4+">"+final_permuted_block.get_hex_string())
        return final_permuted_block

    def encrypt(self,plain_text_block):
        '''
        Encrypts using DES Algorithm.
  
        Parameters: 
        plain_text_block (BitBlock) : plain text block of 64 bits to be encrypted
    
        Returns: 
        cipher_text_block (BitBlock) : cipher text block of 64 bits 
            
        '''
        cipher_block = self.process_fiestal_structure(plain_text_block,is_encryption=True)
        return cipher_block
        
    def decrypt(self,cipher_text_block):
        '''
        Encrypts using DES Algorithm.
  
        Parameters: 
        cipher_text_block (BitBlock) : plain text block of 64 bits to be encrypted
    
        Returns: 
        cipher_text_block (BitBlock) : cipher text block of 64 bits 
            
        '''
        plain_text_block = self.process_fiestal_structure(cipher_text_block,is_encryption=False)
        return plain_text_block

    @staticmethod
    def test():
        descrypto_obj_1 = DESCryptography("FEDCBA9876543210")
        plain_text_block = BitBlock("AB123456CDEF7890")
        print("-"*25)
        print("Plain text:\n"+"-"*4+">"+plain_text_block.get_hex_string())
        print("-"*25)
        cipher_block = descrypto_obj_1.encrypt(plain_text_block)
        print("-"*25)
        print("cipher text:\n"+"-"*4+">"+cipher_block.get_hex_string())
        print("-"*25)
        deciphered_block = descrypto_obj_1.decrypt(cipher_block)
        
        print("-"*25)
        print("deciphered text:\n"+"-"*4+">"+deciphered_block.get_hex_string())
        print("-"*25)
    
if __name__ == "__main__":
    #BitBlock.test()#Test phase-1 passed
    #KeyBlock.test()
    DESCryptography.test()