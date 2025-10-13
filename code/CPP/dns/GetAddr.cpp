/*
 * =====================================================================================
 *
 *       Filename:  GetAddr.cpp
 *
 *    Description:  GetAddrinfo 
 *
 *        Version:  1.0
 *        Created:  07/03/2014 10:49:08
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Yosi Izaq
 *   Organization:  
 *
 * =====================================================================================
 */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>


// For getaddrinfo 
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <netinet/in.h> /* for sockaddr_in and sockaddr_in6 */
#include <arpa/inet.h> /* for sockaddr_in and sockaddr_in6 */

// For libresolv
#include <arpa/nameser.h>
#include <resolv.h>

#define _PREF_DCS_RESOLVER_RETRIES 2
#define _PREF_DCS_RESOLVER_TIMEOUT 3
// For getaddrinfo 

int main(int argc, const char *argv[])
{
	char s_name[160];

	if (argc == 1) {
		printf("Please provide name to resolv\n");
		scanf("%s", s_name);
	}
	else if (argc == 2){

		strcpy(s_name, argv[1]);
	}
	printf("name to resolv - %s\n", s_name);

	//Init resolver
	if (RES_INIT) {
		printf("Resolver already initialized \n");
	}
	else {
		
		printf("Resolver not initialized \n");
		if (res_init()) { 
			
			printf("Resolver init failed! \n");
			return 1;
		}
		else {
			
			printf("Resolver initialization succeeded \n");
		}
	}

	// set retries 2, TO 3
	_res.retrans = 3;
	_res.retry = 2;

	struct addrinfo aiHints;
	struct addrinfo *pres, *aiList = NULL;
	int retVal;

	// Setup the hints address info structure
	// which is passed to the getaddrinfo() function
	memset(&aiHints, 0, sizeof(aiHints));
	aiHints.ai_family = AF_INET; // Only IPv4, for IPv6 also set PF_UNSPEC
	aiHints.ai_socktype = SOCK_STREAM; // TCP query
	aiHints.ai_protocol = IPPROTO_TCP;
	 
	// Call getaddrinfo(). If the call succeeds, the aiList variable
	// will hold a linked list f addrinfo structures containing
	// response information about the host
	if ((retVal = getaddrinfo(s_name, NULL, &aiHints, &aiList)) != 0)
	{
	  printf("getaddrinfo() failed with error code %d - error %s.\n", retVal, gai_strerror(retVal));
	}


         struct sockaddr_in  *p_sa4;        /* to manipulate IPv4 addresses */
         struct sockaddr_in6 *p_sa6;        /* to manipulate IPv6 addresses */
         char                 c_v6[42];     /* for max IPv6 address */

	for ( pres = aiList; pres ; pres = pres->ai_next) {
             switch(pres->ai_family)
             {
             case AF_INET: /* IPv4 type */
                 p_sa4 = (struct sockaddr_in *)pres->ai_addr; /* cast to IPv4 socket type */
                 printf("Found domain IPv4 A record %s \n" , inet_ntoa(p_sa4->sin_addr));
                 break;
             case AF_INET6: /* IPv6 type*/
                 p_sa6 = (struct sockaddr_in6 *)pres->ai_addr; /* cast to IPv6 socket type */
                 printf("Found domain IPv6 A record %s  \n", inet_ntop(pres->ai_family, &p_sa6->sin6_addr, c_v6,42) );
                 break;
             default:
                 printf("Found domain A record of unknown ai_family %d\n", pres->ai_family);
                 break;
             }// switch(p_results->ai_family)
	}

	return 0;
}

