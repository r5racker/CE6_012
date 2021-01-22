#include <stdio.h> 
#include <string.h>
#include <stdlib.h> 
#define FRAME_LENGTH 8
char calculateChecksum(char *buff,int count,int length){
	//printf("checksum,%c\n",buff[0]);
	int i = 0;
	char checksum = buff[0];
	for(i=1;i<count;i++){
		checksum = checksum ^ buff[i];
	}
	//printf("checksum end");
	buff[i]=checksum;
	return checksum;
}

int main() 
{ 
	FILE *fptr,*output_stream; 

	int length = FRAME_LENGTH + 1;
    char *buffer,check_sum;
    buffer = (char*)malloc((length+1) * sizeof(char));
	buffer[length]='\n';
	// Open file 
	fptr = fopen("frames_file.txt", "r"); 
	if (fptr == NULL) 
	{ 
		printf("Cannot open file \n"); 
		exit(0); 
	} 

	output_stream = fopen("orignial_receiver.txt", "w"); 
	if (output_stream == NULL) 
	{ 
		printf("Cannot open file \n"); 
		exit(0); 
	}
	// Read contents from file 
	int count = fread(buffer, sizeof(char), length, fptr);
	
	while (count != 0)
	{
		printf("Frame :%s\n",buffer);
		check_sum = calculateChecksum(buffer,count,length);
		//printf("%d",check_sum);
        if(check_sum == 0){
            fwrite(buffer,sizeof(char),count-1,output_stream);
        }else{
            printf("Error found in frame");
            strcpy(buffer,"ERROR");
            fwrite(buffer,sizeof(char),count-1,output_stream);
        }
		strcpy(buffer,"     \n");
		count = fread(buffer, sizeof(char), length , fptr);
	}

	fclose(fptr); 
	fclose(output_stream);
	return 0; 
}