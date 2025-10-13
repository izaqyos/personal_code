/*
 * =====================================================================================
 *
 *       Filename:  basic_threads.cpp
 *
 *    Description:  C++11 threads
 *
 *        Version:  1.0
 *        Created:  05/23/16 14:02:24
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  YOSI IZAQ
 *   Organization:  
 *
 * =====================================================================================
 */
#include <iostream>
#include <string>
#include <thread>

using namespace std;

static const int num_thrs = 10;
void myfunc(int tid){
	cout<<"Thread "<<tid<<endl;
}

int main(){

	thread thrs[num_thrs];
	cout<<"launching threads"<<endl;
	for (int i = 0; i < num_thrs; i++) {
		thrs[i] = thread(myfunc, i);
	}
	cout<<"launched threads"<<endl;

	for (int i = 0; i < num_thrs; i++) {
		thrs[i].join();
	}

	return 0;
}
