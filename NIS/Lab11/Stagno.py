from random import randint
import math
import copy
class Image_Steganography:
    def __init__(self,n):
        self.row_size = n
        self.image_matrix = []
        for i in range(n):
            l = []
            for j in range(n):
                l.append(randint(0, 255))
            self.image_matrix.append(l)
        
    @staticmethod
    def dec_to_bin(n):
        return str(bin(n)[2  :]).zfill(8)
    @staticmethod
    def bin_to_dec(s):
        l = len(s)
        s = s[ : : -1]
        ans = 0
        for i in range(l):
            ans += (2 ** i) * int(s[i])
        return (ans)

    @staticmethod
    def bin_to_hex(bin_string):
        return hex(int(bin_string,2)).replace("0x","").upper()

    def hide_message(self, message):
        batch_size=len(message)//(self.row_size**2)
        print(f"batch_size={batch_size}")
        message_binary = message.zfill(batch_size * (self.row_size**2) )
        encoded = copy.deepcopy(self.image_matrix)
        message_index = 0
        for i in range(self.row_size):
            for j in range(len(encoded[i])):
                value = message_binary[message_index:message_index+batch_size]
                message_index += batch_size
                temp = Image_Steganography.dec_to_bin(encoded[i][j])
                new = temp[ : len(temp) - batch_size] + value
                encoded[i][j] = Image_Steganography.bin_to_dec(new)
        return (encoded)


    def extract_data(self,encoded,bit_encoding):
        string = ""
        for i in range(self.row_size):
            for j in range(len(encoded)):
                string += Image_Steganography.dec_to_bin(encoded[i][j])[-bit_encoding:]
        return string
    
    def calculate_PSNR(self,encoded):
        mse = 0.00
        n = self.row_size
        for i in range(n):
            for j in range(n):
                mse += (self.image_matrix[i][j] - encoded[i][j]) ** 2
                #print("mse",mse)
        
        mse = mse / (n * n)
        PSNR = 10 * math.log10((255 ** 2) / mse)
        return PSNR
    
    @staticmethod
    def generate_random_message(size):
        message = "1"
        for _ in range(size):
            message += str(randint(0, 1))
        message = message[ : len(message) - 1]
        return message

    @staticmethod
    def test(n,display_matrices=False):
        img_stego = Image_Steganography(n)
        print(f"\nGenerating Image of size {n}X{n} = {(n**2)}")
        if(display_matrices):
            print(f"Image\n{img_stego.image_matrix}")
        #case-1: message size == image size 
        message1 = Image_Steganography.generate_random_message(n**2)
        print(f"\nGenerating message1 of size {n*n}")
        if(display_matrices):
            print(f"message1 : {Image_Steganography.bin_to_hex(message1)}")
        encoded_image1 = img_stego.hide_message(message1)
        if(display_matrices):
            print(f"encoded_image_1\n{encoded_image1}")
        PSNR1 = img_stego.calculate_PSNR(encoded_image1)
        print(f"PSNR value for hiding 1 bit  per pixel : {PSNR1}")
        extracted_message1 = img_stego.extract_data(encoded_image1,1)

        #case-2: message size = 2 * image size
        message2 = Image_Steganography.generate_random_message(2*(n**2))
        print(f"\nGenerating message2 of size {2*(n**2)}")
        encoded_image2 = img_stego.hide_message(message2)
        PSNR2 = img_stego.calculate_PSNR(encoded_image2)
        print(f"PSNR value for hiding 2 bits per pixel :  {PSNR2}")
        extracted_message2 = img_stego.extract_data(encoded_image2,2)

        #case-3: message size = 4 * image size
        message3 = Image_Steganography.generate_random_message(4*(n**2))
        print(f"\nGenerating message2 of size {4*(n**2)}")
        encoded_image3 = img_stego.hide_message(message3)
        PSNR3 = img_stego.calculate_PSNR(encoded_image3)
        print(f"PSNR value for hiding 4 bits per pixel : {PSNR3}")
        extracted_message3 = img_stego.extract_data(encoded_image3,4)
        
        #summary
        print(f"\nMessage and extracted are same ? (1 bit per pixel) : {extracted_message1==message1}")
        print(f"Message and extracted are same ? (2 bit per pixel) : {extracted_message2==message2}")
        print(f"Message and extracted are same ? (4 bit per pixel) : {extracted_message3==message3}")

if __name__ == "__main__":
    Image_Steganography.test(8,display_matrices=True)
    Image_Steganography.test(64)