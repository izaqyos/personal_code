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

	while (grade != -1) //sentinel controlled loop. For countr controlled loop use (counter <= value) logic for example
	{
		counter++;
		total+=grade;


		printf ("Please enter grade. -1 to end.\n");
		scanf("%d", &grade);

	}

	if (counter>0 ) 
	{
		average = (float) total/counter; //cast to float to prevent truncation
	}
	else //avoid division by zero
	{
		average = 0;
	}
	printf("You entered %d grades. Average is %.4f\n",counter, average); //print average with four digits of precision

	return EXIT_SUCCESS;
}				/* ----------  end of function main  ---------- */
