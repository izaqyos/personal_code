/*
 * =====================================================================================
 *
 *       Filename:  ip_store_string.cpp
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  03/10/2013  3:00:04 PM
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
#include <arpa/inet.h>
#include <string>

using namespace std;

int main ()
{
	printf ("Test IP to string conversion functions...\n");

	// IPv4 demo of inet_ntop() and inet_pton()
	
	struct sockaddr_in sa;
	void * p_sa = &sa;
	char str[INET_ADDRSTRLEN];
	char str2[INET_ADDRSTRLEN];
	
	// store this IP address in sa:
	inet_pton(AF_INET, "192.0.2.33", &(sa.sin_addr));
	
	string ip_str ((char *) p_sa,sizeof(sa));
	
	// now get it back and print it
	inet_ntop(AF_INET, &(sa.sin_addr), str, INET_ADDRSTRLEN);
	
	printf("IP from sa struct: %s\n", str); // prints "192.0.2.33"

	inet_ntop(AF_INET, ip_str.data(), str2, INET_ADDRSTRLEN);
	printf("IP from std string: %s\n",str2 ); // prints "192.0.2.33"
}

