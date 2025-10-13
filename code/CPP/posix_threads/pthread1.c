/*
 * =====================================================================================
 *
 *       Filename:  pthread1.c
 *
 *    Description:  simple posix threads, based on http://www.yolinux.com/TUTORIALS/LinuxTutorialPosixThreads.html
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

void *prnt_msg_func(void *p);

main()
{
	pthread_t t1, t2;
	char *msg1 = "Hello world 1";
	char *msg2 = "Hello world 2";
	int iret1, iret2;

	/*  Create independent threads each of which will execute function */

	iret1 = pthread_create(&t1, NULL, prnt_msg_func, (void *) msg1);
	iret2 = pthread_create(&t2, NULL, prnt_msg_func, (void *) msg2);

/*  Wait till threads are complete before main continues. Unless we  */
/*  wait we run the risk of executing an exit which will terminate   */
/*  the process and all threads before the threads have completed.   */

	pthread_join(t1, NULL);
	pthread_join(t2, NULL);

	printf("Thread 1 returns: %d\n",iret1);
	printf("Thread 2 returns: %d\n",iret2);

	exit(0);

}

void * prnt_msg_func(void *p)
{
	printf("%s\n", (char *) p);
}
