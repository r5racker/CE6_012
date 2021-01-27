#include <stdio.h>
#include <string.h>
#define DELIMETER_LENGTH 8

int main(void)
{
    FILE *fpStuffedData, *fpUnstuffedFile;
    char ch;
    int i = 0,consecutiveOnes = 0,pendingZeroFlag = 0;

    printf("Unstuffing Bits \n\n");

    if ((fpStuffedData = fopen("BitStuffedData.txt", "r")) == NULL)
    {
        printf("ERROR : Cannot open file\n");
        return (-1);
    }
    if ((fpUnstuffedFile = fopen("BitUnstuffedDataByReceiver.txt", "w")) == NULL)
    {
        printf("ERROR : Cannot open file\n");
        return (-1);
    }
    for(i=0; i< DELIMETER_LENGTH; i++)
        ch = fgetc(fpStuffedData);
    consecutiveOnes = 0;
    while(1)
    {
        ch = fgetc(fpStuffedData);
        if (ch == EOF)
            break;
        if (consecutiveOnes == 5)
        {
            if(ch == '1'){
                break;
            }
            else{
                if(pendingZeroFlag){
                    printf("0");
                    fprintf(fpUnstuffedFile, "0");
                    pendingZeroFlag=0;
                }
                consecutiveOnes = 0;
                printf("11111");
                fprintf(fpUnstuffedFile, "11111");
                ch = fgetc(fpStuffedData);
                i++;
            }  
        }
        if (ch == '1')
        {
            consecutiveOnes++;
        }
        else
        {
            if(pendingZeroFlag){
                printf("0");
                fprintf(fpUnstuffedFile, "%d", 0);
            }
            for(i = 0; i < consecutiveOnes; i++){
                printf("1");
                fprintf(fpUnstuffedFile, "%d", 1);
            }
            
            pendingZeroFlag = 1;
            consecutiveOnes = 0;
        }
    }
    fclose(fpStuffedData);
    fclose(fpUnstuffedFile);
    return 0;
}