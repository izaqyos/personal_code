/*
 * =====================================================================================
 *
 *       Filename:  pthread_race_cond.c
 *
 *    Description:  simple posix threads, based on http://www.yolinux.com/TUTORIALS/LinuxTutorialPosixThreads.html
 *    demo race condition
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

main()
{
	pthread_t t1, t2;
	int iret1, iret2;

	/*  Create independent threads each of which will execute function */

	iret1 = pthread_create(&t1, NULL, func, NULL);
	iret2 = pthread_create(&t2, NULL, func, NULL);

/*  Wait till threads are complete before main continues. Unless we  */
/*  wait we run the risk of executing an exit which will terminate   */
/*  the process and all threads before the threads have completed.   */

	pthread_join(t1, NULL);
	pthread_join(t2, NULL);

	printf("Thread 1 returns: %d\n",iret1);
	printf("Thread 2 returns: %d\n",iret2);

	printf("Final counter value: %d\n",counter);
	exit(0);

}

void * func( void *p)
{
	counter++;
	printf("thread counter %d\n", counter);
}

/*
Just one thread works ok:
[yizaq@yizaq-WS:Tue Sep 11:/cygdrive/c/work/cpp/posix_threads:]$ a.exe
thread counter 1
Thread 1 returns: 0
Final counter value: 1

Two, not always
[yizaq@yizaq-WS:Tue Sep 11:/cygdrive/c/work/cpp/posix_threads:]$ g++ -lpthread pthread_race_cond.c 
[yizaq@yizaq-WS:Tue Sep 11:/cygdrive/c/work/cpp/posix_threads:]$ a.exe
thread counter 1
thread counter 2
Thread 1 returns: 0
Thread 2 returns: 0
Final counter value: 2

thread counter 1
thread counter 2
Thread 1 returns: 0
Thread 2 returns: 0
Final counter value: 0
 
 */
