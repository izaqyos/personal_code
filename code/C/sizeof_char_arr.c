/*
 * =====================================================================================
 *
 *       Filename:  sizeof_char_arr.c
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  06/ 6/2012  5:44:20 PM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  YOUR NAME (), 
 *   Organization:  
 *
 * =====================================================================================
 */
#include <stdlib.h>
#include <stdio.h>


int main ()
{
	struct aaa{
		int b;
		char arr[];
	};

	struct aaa a;
	printf("size of empty char array in struct containing int as well is %d\n", sizeof(a));
}
