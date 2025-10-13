/*
 * =====================================================================================
 *
 *       Filename:  normalizeIPv6Addr.cpp
 *
 *    Description:  
 *
 *
 *        Version:  1.0
 *        Created:  08/06/15 13:58:52
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  YOSI IZAQ
 *   Organization:  
 *
 * =====================================================================================
 */

#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string>

using namespace std;

int normalizeIPV6Addr(const string & ipv6addr, string & normalizedaddr )
{
	cout<<"Got address "<<ipv6addr <<endl;
	unsigned char buf[sizeof(struct in6_addr)];
	int res;
	inet_pton(AF_INET6, ipv6addr.c_str(), buf);
	char str[INET6_ADDRSTRLEN];
	normalizedaddr = "";
	if (res <=0) 
	{
	    if (res == 0 ) 
	    {
	    	cout<<"Address not in presentation format"<<endl;
	    }
	    else
	    {
		    perror("inet_pton");
	    }
	}
	else
	{
		cout<<"Address trandlated to binary"<<endl;
	}

	if (inet_ntop(AF_INET6, buf, str, INET6_ADDRSTRLEN) == NULL ) 
	{
            perror("inet_ntop");
	}

	string sTemp(str);
	normalizedaddr = sTemp;
        cout<<"Normalized address: " << normalizedaddr << " res: "<< res<<endl; 
	return res;
}

int main(int argc, const char *argv[])
{
	string saddr, snormaddr;
	cout<<"Please enter address in IPV6 format"<<endl;
	cin>>saddr;
	cout<<"Got address in IPV6 format:"<<saddr<<endl;

	if ( normalizeIPV6Addr(saddr , snormaddr )  > 0)
	{
           cout<<"Normalized address: " << snormaddr << endl; 
	}
	return 0;
}

