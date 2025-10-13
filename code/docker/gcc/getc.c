/*
 * =====================================================================================
 *
 *       Filename:  getc.c
 *
 *    Description:  
 *
 *
 *        Version:  1.0
 *        Created:  10/27/14 16:17:57
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

main(){
	int c;
	printf("Echo program. Please type...\n");

	long ccount = 0;
	int lcount,scount,tcount = 0;

	while ( (c = getchar() ) != EOF)
	{
		++ccount;
		if ( c == '\n') ++lcount;
		if ( c == ' ') ++scount;
		if ( c == '\t') ++tcount;
		putchar(c);
	}
	printf("Char Count: %ld, Spaces Count: %d, Tabs Count: %d, Line Count: %d\n", ccount, scount, tcount, lcount);
}

