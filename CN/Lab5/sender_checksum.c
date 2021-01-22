#include <stdio.h> 
#include <string.h>
#include <stdlib.h> 

char calculateChecksum(char *buff,int count,int length){
	if(count>length){
		exit(-1);
	}
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

	int frame_length = 8;
	//char filename[100];
    char *buffer,check_sum;
	buffer = (char*)malloc((frame_length+2)*sizeof(char));
	buffer[frame_length+1] = '\n';
	// Open file 
	fptr = fopen("original.txt", "r"); 
	if (fptr == NULL) 
	{ 
		printf("Cannot open file \n"); 
		exit(0); 
	} 

	output_stream = fopen("frames_file.txt", "w"); 
	if (fptr == NULL) 
	{ 
		printf("Cannot open file \n"); 
		exit(0); 
	}

	// Read contents from file 
	//c = fgetc(fptr);
	int count = fread(buffer, sizeof(char), frame_length, fptr);
	while (count != 0) 
	{
		buffer[frame_length]=' ';
		printf("_________\n");
		printf("Frame :%s",buffer);
		check_sum = calculateChecksum(buffer,count,frame_length);
		printf("checksum: %d\n",check_sum);
		fwrite(buffer,sizeof(char),count+1,output_stream);
		strcpy(buffer,"     \n");
		count = fread(buffer, sizeof(char), frame_length, fptr);
	}

	fclose(fptr); 
	fclose(output_stream);
	return 0; 
}