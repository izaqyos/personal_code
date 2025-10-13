/*
 * =====================================================================================
 *
 *       Filename:  server.c
 *
 *    Description:  simple echo server that uses select
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
#include <sys/time.h> //FD_xxx macros for select
#include <errno.h> //for errno

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

	int clients_sockets[30], max_clients = 30;
	for (int i=0;i<max_clients;++i) //init to 0 , which signals not used
		clients_sockets[i]=0;



	socketfd = socket(AF_INET, SOCK_STREAM, 0);// Domain - internet, type - stream/tcp, protocl, default (PF_INET in AF_INET case) . This is main socket
	if (socketfd < 0 ) error("Can't create socket");
	int opt = 1; //true
	if (setsockopt(socketfd, SOL_SOCKET, SO_REUSEADDR, (char *) &opt, sizeof(opt)) < 0) 
	{
		error("Fail to set socket options accept multiple connections");
		exit(1);
	}

	memset(&srv_addr, 0, sizeof(srv_addr)); 
	portnum = atoi(argv[1]);

	// set srv_addr for bind
	srv_addr.sin_family = AF_INET;
	srv_addr.sin_addr.s_addr= INADDR_ANY; // local address, for specific address use inet_aton, ex: inet_aton("1.2.3.4", &srv_addr.sin_addr) . for ipv6 use inet_pton
	srv_addr.sin_port = htons(portnum); // must convert to network order

	if (bind(socketfd, (struct sockaddr *) &srv_addr, sizeof(srv_addr)) < 0 )  error ("Couldn't bind to socket!");//bind socket to address+port

	printf("Listening on port %d\n", portnum);
	if (listen(socketfd,10) < 0)  //blocking, connection Q size 10
	{
		error("Listen call has failed");
		exit(1);
	}

	client_len = sizeof(cli_addr);
	char * msg = "Welcome to ECHO Select server\r\n";

	printf("Server waiting for connections...\n");

	fd_set readfds;
	int max_sd, activity; //select requires max fd... , select return code

	while (1)
	{
		FD_ZERO(&readfds);
		FD_SET(socketfd, &readfds); //add master socket
		max_sd = socketfd;

		//add connection sockets if any to fd set
		for (int i=0;i<max_clients;++i) 
		{
			if(clients_sockets[i] > 0) // initialized socket
			{
				FD_SET(clients_sockets[i], &readfds);
			}
			if (clients_sockets[i] > max_sd) max_sd = clients_sockets[i];
		}

		activity = select(max_sd+1, &readfds, NULL,NULL,NULL);
		if ( (activity < 0 ) && (errno != EINTR))
		{
			error("select error");
			exit(1);
		}

		if (FD_ISSET(socketfd, &readfds)) // incoming connections are on socketfd...
		{
			nsocketfd = accept(socketfd, (struct sockaddr *) &cli_addr, &client_len); //accept incoming connection
			if (nsocketfd < 0) error ("Failed to accept incoming connection");
			printf("Established connection from address %s, port %d, socket fd: %d \n", inet_ntoa(cli_addr.sin_addr), ntohs(cli_addr.sin_port), nsocketfd);

			if(send(nsocketfd, msg, strlen(msg),0) !=strlen(msg))
			{

				error("Send failed");
			 }

			for (int i=0;i<max_clients;++i) 
			{
				if(clients_sockets[i] == 0) // uninitialized socket
				{
					clients_sockets[i] = nsocketfd;
					printf("Adding socket %d to set at index %d\n", nsocketfd, i);
					break;

				}
			}
//			cpid = fork();
//			if (cpid < 0) error("fork error");
//
//			if(cpid == 0) // child
//			{
//				printf("Forke handler child\n");
//				close(socketfd);
//				servClient(nsocketfd);
//				close(nsocketfd);
//				exit(0);
//
//			}
//			else
//			{
//				close(nsocketfd);
//			}

		}

		int valread;
		for (int i=0;i<max_clients;++i) // Check incoming data on client sockets
		{
			int sd = clients_sockets[i];

			if(FD_ISSET(sd,&readfds))
			{

				if( (valread = read(sd,buffer,1024)) == 0) //read incoming msg, 0 ret val means close
				{
					getpeername(sd, (struct sockaddr *) &cli_addr, (socklen_t *) &client_len); // get sockaddr_in data from socket
					printf("Got disconnect from ip %s, port %d\n", inet_ntoa(cli_addr.sin_addr), ntohs(cli_addr.sin_port));
					close(sd);
					clients_sockets[i]=0;

				}
				else //regular msg
				{
					//echo back
					buffer[valread] = '\0'; //set null at end of read msg
					send(sd,buffer,strlen(buffer),0);
				}
			}
		}


	}

	close(socketfd);
	return 0;

}

