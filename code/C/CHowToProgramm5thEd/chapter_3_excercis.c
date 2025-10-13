/*
 * =====================================================================================
 *
 *       Filename:  chapter_3_excercis.c
 *
 *    Description:  Ansers to:
 *    Self-Review Exercises
 * 3.1 Fill in the blanks in each of the following questions.
 * a) A procedure for solving a problem in terms of the actions to be executed and the order
 * in which the actions should be executed is called a(n) .
 * b) Specifying the execution order of statements by the computer is called .
 * c) All programs can be written in terms of three types of control statements: ,
 * and .
 * d) The selection statement is used to execute one action when a condition is
 * true and another action when that condition is false.
 * e) Several statements grouped together in braces ({ and }) are called a(n) .
 * f) The repetition statement specifies that a statement or group of statements
 * is to be executed repeatedly while some condition remains true.
 * g) Repetition of a set of instructions a specific number of times is called repetition.
 * h) When it is not known in advance how many times a set of statements will be repeated,
 * a(n) value can be used to terminate the repetition.
 * 3.2 Write four different C statements that each add 1 to integer variable x.
 * 3.3 Write a single C statement to accomplish each of the following:
 * a) Assign the sum of x and y to z and increment the value of x by 1 after the calculation.
 * b) Multiply the variable product by 2 using the *= operator.
 * c) Multiply the variable product by 2 using the = and * operators.
 * d) Test if the value of the variable count is greater than 10. If it is, print “Count is greater
 * than 10.”
 * e) Decrement the variable x by 1, then subtract it from the variable total.
 * f) Add the variable x to the variable total, then decrement x by 1.
 * g) Calculate the remainder after q is divided by divisor and assign the result to q. Write
 * this statement two different ways.
 * h) Print the value 123.4567 with 2 digits of precision. What value is printed?
 * i) Print the floating-point value 3.14159 with three digits to the right of the decimal point.
 * What value is printed?
 * 3.4 Write a C statement to accomplish each of the following tasks.
 * a) Define variables sum and x to be of type int.
 * b) Initialize variable x to 1.
 * c) Initialize variable sum to 0.
 * d) Add variable x to variable sum and assign the result to variable sum.
 * e) Print "The sum is: " followed by the value of variable sum.
 * 3.5 Combine the statements that you wrote in Exercise 3.4 into a program that calculates the
 * sum of the integers from 1 to 10. Use the while statement to loop through the calculation and increment
 * statements. The loop should terminate when the value of x becomes 11.
 * 3.6 Determine the values of variables product and x after the following calculation is performed.
 * Assume that product and x each have the value 5 when the statement begins executing.
 * product *= x++;
 * 3.7 Write single C statements that
 * a) Input integer variable x with scanf.
 * b) Input integer variable y with scanf.
 * c) Initialize integer variable i to 1.
 * d) Initialize integer variable power to 1.
 * e) Multiply variable power by x and assign the result to power.
 * f) Increment variable i by 1.
 * g) Test i to see if it is less than or equal to y in the condition of a while statement.
 * h) Output integer variable power with printf.
 * 3.8 Write a C program that uses the statements in Exercise 3.7 to calculate x raised to the y power.
 * The program should have a while repetition control statement.
 * 3.9 Identify and correct the errors in each of the following:
 * a) while ( c <= 5 ) {
 * product *= c;
 * ++c;
 * b) scanf( "%.4f", &value );
 * c) if ( gender == 1 )
 * printf( "Woman\n" );
 * else;
 * printf( "Man\n" );
 * 3.10 What is wrong with the following while repetition statement (assume z has value 100),
 * which is supposed to calculate the sum of the integers from 100 down to 1:
 * while ( z >= 0 )
 * sum += z;
 *
 *        Version:  1.0
 *        Created:  08/21/11 14:47:31
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
	int x = 0;
	int y = 0;
	int z = 0;
	int count = 6;
	int total = 0;
	int divisor = 2;
	int quotient = 5;

	//Four ways to increment
	++x;
	x++;
	x = x +1;
	x +=1;

	z=x++ +y ;
	z*=2;
	z = z*2;
	if (count>=10) printf("count is greater than 10\n");
	total -= --x;
	total+=x--;
	quotient = quotient % divisor;
	quotient %= divisor;
	printf("%.2f\n",123.4567);
	printf("%.3f\n",3.14159);

	int sum=0;
	x=1;
	sum+=x;
	printf("sum: %d\n", sum);


	while ( x < 11 )
	{
		sum+=x++;
	}
	printf("sum: %d\n", sum);


	printf ("Please enter value for x.\n");
	scanf("%d", &x);
	printf ("Please enter value for y.\n");
	scanf("%d", &y);
	int i=1;
	int power=1;
	power*=x;
	i++;
	while (i++<=y){
		power*=x;
	}

	printf("power: %d\n");

	return EXIT_SUCCESS;
}				/* ----------  end of function main  ---------- */
