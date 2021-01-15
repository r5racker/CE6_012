#include <stdio.h> 
#include <string.h>
#include <stdlib.h> 

char calculateChecksum(char buff[],int count,int length){
	int i = 0;
	char checksum = buff[0];
	for(i=1;i<count;i++){
		checksum = checksum ^ buff[i];
	}
	buff[i]=checksum;
	return checksum;
}

int main() 
{ 
	FILE *fptr,*output_stream; 

	int length = 8;
	//char filename[100];
    char buffer[9],check_sum;

	// Open file 
	fptr = fopen("F:\\desktop_files_repo\\prog\\012_sem6\\CN\\Lab5\\original.txt", "r"); 
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
	int count = fread(&buffer, sizeof(char), 8, fptr);
	while (count != 0) 
	{
		check_sum = calculateChecksum(buffer,count,8);
		fwrite(buffer,sizeof(char),count+1,output_stream);
		count = fread(&buffer, sizeof(char), 8, fptr);
	}

	fclose(fptr); 
	fclose(output_stream);
	//printf("\n|%c|",1);
	return 0; 
}