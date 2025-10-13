/*
 * =====================================================================================
 *
 *       Filename:  future_101.cpp
 *
 *    Description:  playground for future, async and promise
 *
 *        Version:  1.0
 *        Created:  Sun Apr  9 12:23:37 IDT 2017
 *       Revision:  none
 *       Compiler:  clang++ -std=c++11
 *
 *         Author:  Yosi Izaq
 *   Organization:  
 *
 * =====================================================================================
 */
/*
 * 

[yizaq@YIZAQ-M-W1ZV:Sun Apr 09:~/Desktop/Work/code/C11/future:]$ clang++ -std=c++11 future_promise.cpp  -o future_promise
[yizaq@YIZAQ-M-W1ZV:Sun Apr 09:~/Desktop/Work/code/C11/future:]$ ./future_promise 
Creating promise and waiting for thread2 to complete...
Thread1 waiting for promised future object from thread 2
value: 10

 */
#include <iostream>
#include <vector>
#include <future>
#include <thread>
#include <chrono>

using namespace std;

void thread1Func()
{
	cout<<"Creating promise and waiting for thread2 to complete..."<<endl;
	promise<int> intProm;
	future<int> intFut = intProm.get_future();
	thread thread2([](promise<int> * prom){ cout<<"thread 2"<<endl<<"value: "; this_thread::sleep_for(chrono::seconds(2));prom->set_value(10);}, &intProm);
	cout<<"Thread1 waiting for promised future object from "<<intFut.get()<<endl;//This will block untill intFut has a value

	thread2.join();
}

int main()
{

	thread th1(thread1Func);

	th1.join();

	return 0;

}
