/*
 * =====================================================================================
 *
 *       Filename:  simple_templates.cpp
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  05/28/15 14:58:24
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  YOSI IZAQ
 *   Organization:  
 *
 * =====================================================================================
 */
#include <stdlib.h>
//#include <stdio.h>
#include<iostream>

using namespace std;

template <class T> 
void printNtimes(T num, unsigned int n)
{
	cout <<num*n<<endl;
}

int main(int argc, const char *argv[])
{
	printNtimes(3,5);
	printNtimes(3.21,5);
	return 0;
}

