/*
 * =====================================================================================
 *
 *       Filename:  average.c
 *
 *    Description:  calculate average using sentinel controlled repetition
 *
 *        Version:  1.0
 *        Created:  08/21/11 10:03:34
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Yosi Izaq (), yizaq@cisco.com
 *        Company:  CISCO
 *
 * =====================================================================================
 */


#include	<stdlib.h>
#include	<stdio.h>

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  main
 *  Description:  
 * =====================================================================================
 */
	int
main ( int argc, char *argv[] )
{
	int counter = 0;
	int total = 0;
	int grade = 0;
	float average = 0;


	printf ("Please enter grade. -1 to end.\n");
	scanf("%d", &grade);

	while (grade != -1)
	{
		counter++;
		total+=grade;


		printf ("Please enter grade. -1 to end.\n");
		scanf("%d", &grade);

	}

	if (counter>0 ) 
	{
		average = total/counter
	}
	else
	{
		average = 0;
	}
	printf("You entered %d grades. Average is %f",counter, average);

	return EXIT_SUCCESS;
}				/* ----------  end of function main  ---------- */
