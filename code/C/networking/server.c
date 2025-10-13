/*
 * =====================================================================================
 *
 *       Filename:  server.c
 *
 *    Description:  simple echo server
 *
 *        Version:  1.0
 *        Created:  03/12/2017 14:33:38
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  YOSI IZAQ
 *   Organization:  
 *
 * =====================================================================================
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

void error( const char * msg)
{
	printf("got error: %s\n", msg);
	perror(msg);
	exit(1);
}

void servClient(int sfd)
{
	char buffer[1024];
	int ret;

	//send(sfd, "> ",25,0); //send str, 25 bytes
	memset(buffer, 0 , 1024);
	ret = recv(sfd, buffer, 1023, 0);	
	if (ret<0) error("Error reading from socket");
	printf("Got %s, len %lu \n", buffer,strlen(buffer));

	while (strncmp("exit",buffer, strlen("exit"))  != 0)
	{
		//echo back
		send(sfd,buffer,strlen(buffer),0); 
		printf("Sent %s\n", buffer);

		memset(buffer, 0 , 1024);
		ret = recv(sfd, buffer, 1023, 0);	
		if (ret<0) error("Error reading from socket");
		printf("Got %s, len %lu \n", buffer,strlen(buffer));
	}

	printf("ending session\n");
	send(sfd,"ending session",strlen("ending session"),0); 
	return;
}

int main (int argc, char * argv[])
{
	if (argc<2)
	{
		printf("usage: %s port\n", argv[0]);
		exit(0);
	}

	int socketfd,  nsocketfd, portnum;

	socklen_t client_len;
	char buffer[1024];
	struct sockaddr_in  srv_addr, cli_addr;
	int ret;
	int cpid;

	socketfd = socket(AF_INET, SOCK_STREAM, 0);// Domain - internet, type - stream/tcp, protocl, default (PF_INET in AF_INET case)
	if (socketfd < 0 ) error("Can't create socket");

	memset(&srv_addr, 0, sizeof(srv_addr)); 
	portnum = atoi(argv[1]);

	// set srv_addr for bind
	srv_addr.sin_family = AF_INET;
	srv_addr.sin_addr.s_addr= INADDR_ANY; // local address, for specific address use inet_aton, ex: inet_aton("1.2.3.4", &srv_addr.sin_addr) . for ipv6 use inet_pton
	srv_addr.sin_port = htons(portnum); // must convert to network order

	if (bind(socketfd, (struct sockaddr *) &srv_addr, sizeof(srv_addr)) < 0 )  error ("Couldn't bind to socket!");//bind socket to address+port

	listen(socketfd,10); //blocking, connection Q size 10

	client_len = sizeof(cli_addr);


	while (1)
	{
		nsocketfd = accept(socketfd, (struct sockaddr *) &cli_addr, &client_len); //accept incoming connection
		if (nsocketfd < 0) error ("Failed to accept incoming connection");
		printf("Established connection from address %s, port %d \n", inet_ntoa(cli_addr.sin_addr), ntohs(cli_addr.sin_port));

		cpid = fork();
		if (cpid < 0) error("fork error");

		if(cpid == 0) // child
		{
			printf("Forket handler child\n");
			close(socketfd);
			servClient(nsocketfd);
			close(nsocketfd);
			exit(0);
		}
		else
		{
			close(nsocketfd);
		}

	}

	close(nsocketfd);
	close(socketfd);
	return 0;

}

