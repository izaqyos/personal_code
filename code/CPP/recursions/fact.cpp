/*
 * =====================================================================================
 *
 *       Filename:  fact.cpp
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  06/30/15 17:35:06
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  YOSI IZAQ
 *   Organization:  
 *
 * =====================================================================================
 */
#include <stdlib.h>
#include <iostream>

using namespace std;

unsigned int fact(unsigned int n)
{
	if (n==0) { return 1;}
	return n*fact(n-1);
}

int main(int argc, const char *argv[])
{

	unsigned int num = 1;
	while (num != 0)
	{
	    cout<<"Plz enter number. 0 to end"<<endl;
	    cin>>num;
	    cout<<num<<" factorial is "<<fact(num)<<endl<<endl;

	}
	return 0;
}
