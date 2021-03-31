// Server
#include <unistd.h> 
#include <stdio.h> 
#include <sys/socket.h> 
#include <stdlib.h> 
#include <netinet/in.h> 
#include <string.h> 
#define PORT 8080 
int main(int argc, char const *argv[]) 
{ 
	int server_fd, new_socket, valread; 
	struct sockaddr_in address; 
	int opt = 1; 
	int addrlen = sizeof(address); 
	char buffer[1024] = {0}; 
	char msg[50];
	
	// Creating socket file descriptor 
	if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) 
	{ 
		perror("socket failed"); 
		exit(EXIT_FAILURE); 
	} 
	
	// Forcefully attaching socket to the port 8080 
	if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT,&opt, sizeof(opt)))
	{ 
		perror("setsockopt"); 
		exit(EXIT_FAILURE); 
	} 
	address.sin_family = AF_INET; 
	address.sin_addr.s_addr = INADDR_ANY; 
	address.sin_port = htons( PORT ); 
	
	// Forcefully attaching socket to the port 8080 
	if (bind(server_fd, (struct sockaddr *)&address,sizeof(address))<0) 
	{ 
		perror("bind failed"); 
		exit(EXIT_FAILURE); 
	} 
	if (listen(server_fd, 3) < 0) 
	{ 
		perror("listen"); 
		exit(EXIT_FAILURE); 
	}
	
	int pid = 0;	
	
       	while(1){	
		if ((new_socket = accept(server_fd, (struct sockaddr *)&address,(socklen_t*)&addrlen))<0) 
		{ 
			perror("accept"); 
			exit(EXIT_FAILURE); 
		} 
		pid = fork();
		if(pid==0){
			close(server_fd);
			//printf("Hello message sent\n"); 			
			printf("-->P-%d Connected to Client\n",getpid());
			//create a new fork process
			bzero(msg,sizeof(msg));
	       		strcpy(msg,"Hello from server\0"); 
			valread = read( new_socket , buffer, 1024); 
			printf("%s\n",buffer ); 
			send(new_socket , msg , strlen(msg) , 0 ); 
			//printf("Hello message sent\n");
			while(valread>0 && strcmp(msg,"<END>")!=0){
				bzero(buffer,sizeof(buffer));
				valread = read( new_socket , buffer, 1024); 
				printf("\t:p-%d received\n",getpid());
				printf("\t%s\n",buffer ); 
			}
			//fork goes out
			printf("<--P-%d Ending connection\n",getpid());
			close(new_socket);
			exit(0);
		}
		close(new_socket);
	}
	close(server_fd);
	return 0; 
} 

