/*
 * =====================================================================================
 *
 *       Filename:  pthread_mutex1.c
 *
 *    Description:  simple posix threads, based on http://www.yolinux.com/TUTORIALS/LinuxTutorialPosixThreads.html
 *    demo mutex
 *
 *        Version:  1.0
 *        Created:  09/11/2012  3:03:13 PM
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
#include <pthread.h>

void *func( void *p);
int counter = 0;
pthread_mutex_t mutex1 = PTHREAD_MUTEX_INITIALIZER;

main()
{
	pthread_t t1, t2;
	int iret1, iret2;

	/*  Create independent threads each of which will execute function */

	if (iret1 = pthread_create(&t1, NULL, func, NULL))
	{
		printf("Thread creation has failed due to error: %d\n",iret1);
	}

	if (iret2 = pthread_create(&t2, NULL, func, NULL))
	{
		printf("Thread creation has failed due to error: %d\n",iret2);
	}

/*  Wait till threads are complete before main continues. Unless we  */
/*  wait we run the risk of executing an exit which will terminate   */
/*  the process and all threads before the threads have completed.   */

	pthread_join(t1, NULL);
	pthread_join(t2, NULL);

	printf("Final counter value: %d\n",counter);
	exit(0);

}

void * func( void *p)
{
	pthread_mutex_lock(&mutex1);
	counter++;
	printf("thread counter %d\n", counter);
	pthread_mutex_unlock(&mutex1);
}
