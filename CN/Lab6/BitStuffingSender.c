#include <stdio.h>
#include <string.h>

int main(void)
{
    FILE *fpOriginalFile, *fpBitStuffedData;
    char inChar;
    int i = 0;
    int consecutiveOnes = 0;

    printf("Stuffing Bits inside data \n");
    if ((fpOriginalFile = fopen("original.txt", "r")) == NULL)
    {
        printf("ERROR : Cannot open file original\n");
        return (-1);
    }
    if ((fpBitStuffedData = fopen("BitStuffedData.txt", "w")) == NULL)
    {
        printf("ERROR : Cannot open file\n");
        return (-1);
    }
    printf("Binary After Stuffing :\n\n");

    fprintf(fpBitStuffedData, "%s", "01111110");
    printf("01111110 ");
    inChar = fgetc(fpOriginalFile);
    printf("%c",inChar);
    while(inChar != EOF)
    {
        if (consecutiveOnes == 5)
        {
            fprintf(fpBitStuffedData, "0");
        }
        if (inChar == '1')
            consecutiveOnes++;
        else
            consecutiveOnes = 0;
        fprintf(fpBitStuffedData, "%c", inChar);
        printf("%c",inChar);
        inChar = fgetc(fpOriginalFile);
    }
    fprintf(fpBitStuffedData, "%s", "01111110");
    printf(" 01111110\n");
    fclose(fpBitStuffedData);
    return 0;
}