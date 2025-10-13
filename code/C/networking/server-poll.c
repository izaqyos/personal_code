/*
 * =====================================================================================
 *
 *       Filename:  server-poll.c
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
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/time.h> //FD_xxx macros for select
#include <sys/poll.h> //for poll
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
	if (setsockopt(socketfd, SOL_SOCKET, SO_REUSEADDR, (char *) &opt, sizeof(opt)) < 0)  //set socket fd to be reusable
	{
		error("Fail to set socket options reusable and accept multiple connections");
		exit(1);
	}

	if ( ioctl(socketfd, FIONBIO,(char *) &opt) < 0 ) //set non blocking socket
	{
		error("Fail to set socket options to non blocking");
		exit(1);
	}
	


	memset(&srv_addr, 0, sizeof(srv_addr)); 
	portnum = atoi(argv[1]);// in c++ use boost lexical_cast

	// set srv_addr for bind
	srv_addr.sin_family = AF_INET; //set AF_INET6 for ipv6 addr
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
	char * msg = "Welcome to ECHO Poll server\r\n";

	printf("Server waiting for connections...\n");

	struct pollfd fds[200];
	int nfds=1,fds_size=0,idx1,idx2,timeout, end_server=0, close_con=0, compress_fds=0;
	memset(fds,0,sizeof(fds));

	//set master socket fd
	fds[0].fd = socketfd;
	fds[0].events = POLLIN;

	timeout = 3*60*1000;//3min in millesconds. 

	while (end_server == 0)
	{

		printf("Polling socket fds\n");
		ret = poll(fds, nfds, timeout); // poll fds, TO set to 3 min...
		if (ret < 1)
		{
			error("Poll call has failed");
			break;
		}
		if (ret == 0)
		{
			error("Poll has timedout, ending...");
			break;
		}

		// 1 < readable fds, check which
		fds_size = nfds;
		for (int i=0;i<fds_size;++i) 
		{
			if (fds[i].revents == 0) continue; //skip non readable
			if (fds[i].revents != POLLIN)  // should be POLLIN, other values are exception
			{
				error("got an unexpected poll revents value");
				end_server = 1;//end server
				break;
			}

			//At this point is all kosher
			if (fds[i].fd == socketfd) // got incoming connection on master socket
			{
				printf("Got one or more incoming connections\n");
				do
				{

					nsocketfd = accept(socketfd, (struct sockaddr *) &cli_addr, &client_len); //accept incoming connection
					if (nsocketfd < 0) //error, on EWOULDBLOCK is ok since it means all new connections were accepted
					{
						if (errno != EWOULDBLOCK)
						{
							error("accept failed");
							end_server = 1;
						}
						break;
					}

				printf("Established connection from address %s, port %d, socket fd: %d \n", inet_ntoa(cli_addr.sin_addr), ntohs(cli_addr.sin_port), nsocketfd);
				fds[nfds].fd = nsocketfd;
				fds[nfds].events = POLLIN;
				nfds++;
				}
				while (nsocketfd != -1);

			}
			else //connection socket
			{
				printf("Socked fd %d is available for read\n", fds[i].fd);
				close_con = 0;

				//read all incoming data 
				do
				{
					ret = recv(fds[i].fd, buffer, sizeof(buffer),0);
					if (ret < 0) //error
					{
						if (errno != EWOULDBLOCK) 
						{
							error("recv failed");
							close_con = i; // the actual socket fd for later close
						}

						// ret == EWOULDBLOCK , meaning finished reading
						break;

					}

					if (ret == 0) // client wants to close connection
					{

						close_con = 1;// the actual socket fd for later close
						printf("connection closed\n");
					}

					//At this point is all kosher, we have real data
					printf("recv got %d bytes\n",ret);
					ret = send(fds[i].fd, buffer, ret, 0);
					if (errno < 0)
					{
						error("send failed\n");
						close_con = 1;// the actual socket fd for later close
						break;
					}

				}
				while (1);

				if (close_con)
				{
					close(fds[close_con].fd);
					fds[close_con].fd = -1;
					compress_fds = 1;

				}


			}//read available on connection

		}// loop pollable fds

		if (compress_fds) // 1< fds were closed. removed from fds array
		{
			compress_fds = 0; 
			for (int i=0; i<nfds;++i)
			{
				if(fds[i].fd == -1)
				{
					for (int j=i;j<nfds;++j)
					{
						fds[j].fd = fds[j+1].fd; 
						//fds[j].events = fds[j+1].events;  // not required since all are POLLIN
						//fds[j].revents = fds[j+1].revents; // not required since a. all are POLLIN , b. revents is output
					}
				}
			}
		}
	}

	//general cleanup
	for (int i=0; i<nfds;++i)
	{
		if(fds[i].fd >=0) close(fds[i].fd);
	}
	
	return 0;

}

