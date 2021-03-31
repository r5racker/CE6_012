// Client 
#include <stdio.h> 
#include <sys/socket.h> 
#include <arpa/inet.h> 
#include <unistd.h> 
#include <string.h> 
#include <sys/types.h>
#define PORT 8080 

int main(int argc, char const *argv[]) 
{ 
    int client_socket = 0, valread; 
    struct sockaddr_in server_addr; 
    char msg[50],pid_str[10];
    sprintf(pid_str, "%ld", getpid());
    printf("client pid-%s\n",pid_str);
    strcpy(msg,"Greetings from client c-");
    strcat(msg, pid_str); 
    char buffer[1024] = {0}; 
    client_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (client_socket < 0) 
    { 
        printf("\n error in creating socket \n"); 
        return -1; 
    } 
    
    server_addr.sin_family = AF_INET; 
    server_addr.sin_port = htons(PORT); 
       
    // Convert IPv4 and IPv6 addresses from text to binary form 
    if(inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr)<=0)  
    { 
        printf("\nInvalid address/ Address not supported \n"); 
        return -1; 
    } 
   
    if (connect(client_socket, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) 
    { 
        printf("\nConnection Failed \n"); 
        return -1; 
    } 
    send(client_socket , msg , strlen(msg) , 0 ); 
    bzero(buffer,sizeof(buffer));
    valread = read( client_socket , buffer, 1024); 
    printf("%s\n",buffer );
    valread=1;
    while(valread>0 && strcmp(msg,"<END>")!=0){
	bzero(msg,sizeof(msg));
	scanf("%[^\n]%*c",msg);
	send(client_socket,msg,strlen(msg),0);
    }
    close(client_socket);
    return 0;
} 
