/*
 * =====================================================================================
 *
 *       Filename:  pthread_cond_vars.c
 *
 *    Description:  illustrate thread synchronization via conditinal variables
 *
 *        Version:  1.0
 *        Created:  03/26/2017 12:09:20
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

pthread_mutex_t cond_mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond_var = PTHREAD_COND_INITIALIZER;

void * f1();
void *f2();
#define STOP_COND 10
#define COND1     3
#define COND2     6
int count = 0;

int main()
{
	pthread_t t1,t2;
	pthread_create(&t1, NULL, f1, NULL); // pthread_t * thread, flags IIRC pthread_attr_t *, void *(*func)(void *) - ptr to void * func(void *) function, void * arguments
	pthread_create(&t2, NULL, f2, NULL); 

	pthread_join(t1, NULL);
	pthread_join(t2, NULL);

	printf("Final count is %d\n", count);
	exit(0);
}

void * f1()
{

	while (1)
	{
		//mutex for protection cond_var, otherwise can have deadlock in race cond where t2 fires cond_var signal before t1 has the chance to wait on it. Then t1 will wait forever for signal that will never come :(
		pthread_mutex_lock(&cond_mutex);

		//only proceed execution when f2 signals cond_var...
		pthread_cond_wait(&cond_var, &cond_mutex);
		count++;
		printf("f1: counter %d\n", count);

		pthread_mutex_unlock(&cond_mutex);
		if (count >= STOP_COND) return(NULL);
	}
}

void * f2()
{

	while (1)
	{
		//mutex for protection cond_var, otherwise can have deadlock in race cond where t2 fires cond_var signal before t1 has the chance to wait on it. Then t1 will wait forever for signal that will never come :(
		pthread_mutex_lock(&cond_mutex);

		//for numbers 1-3 and 8-10 signal to f1 to increment
		//note, race conditions invloving count are possible since it can't be mutexed w/o deadlock
		if (( count < COND1) || (count > COND2))
		{
			pthread_cond_signal(&cond_var);
		}
		else
		{
			count++;
			printf("f2: counter %d\n", count);
		}

		pthread_mutex_unlock(&cond_mutex);
		if (count >= STOP_COND) return(NULL);
	}
}
