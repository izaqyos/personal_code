/*
 * =====================================================================================
 *
 *       Filename:  client.c
 *
 *    Description:  simple client
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

int main (int argc, char * argv[])
{
	int sfd,pnum,ret;
	struct sockaddr_in srvaddr;
	char buf[1024];
	if (argc<3)
	{
		printf("usage: %s server_address port\n", argv[0]);
		exit(0);
	}

	pnum=atoi(argv[2]);

	sfd=socket(AF_INET,SOCK_STREAM,0);

	if(sfd<0) error("can't create socket");

	srvaddr.sin_family=AF_INET;
	srvaddr.sin_port=htons(pnum);
	ret = inet_pton(AF_INET, argv[1],  &srvaddr.sin_addr.s_addr);
	if (ret == 0) error("invalid address");
	else if (ret < 0) error("inet_pton failed");

	int numgot = 0;
	if ( connect(sfd, (struct sockaddr *) &srvaddr, sizeof(srvaddr)) < 0) error("failed 2 connect");
	while (1)
	{
		printf("What to send?");
		memset(buf, 0 , 1024);
		fgets(buf, 1023, stdin);
		ret = write(sfd, buf, strlen(buf));
		if (ret < 0) error ("write to socket failed");

		memset(buf, 0 , 1024);
		ret = recv(sfd, buf, 1023, 0);
		if (ret < 0) error ("read to socket failed");
		printf("Got %s\n",buf);
		numgot++;
		
		if(numgot == 5)
		{
			close(sfd);
			return 0;
		}
	}
}
