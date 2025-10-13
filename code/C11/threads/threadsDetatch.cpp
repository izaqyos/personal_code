/*
 * =====================================================================================
 *
 *       Filename:  threadsDetatch.cpp
 *
 *    Description:  play w/ join and detach
clang++ -std=c++11 threadsDetatch.cpp  -o threadsDetatch
 *
 *        Version:  1.0
 *        Created:  03/28/2017 14:58:17
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Yosi Izaq
 *   Organization:  
 *
 * =====================================================================================
 */
#include <iostream>
#include <thread>
#include <vector>
#include <algorithm> //for_each
#include <functional> //mem_fn (calls member function of input class instance by creating a wrapper...

using namespace std;

void thrFunc()
{
	for (int i=0;i<10000;++i) cout<<"Thread "<<this_thread::get_id()<<"running..."<<endl;
}

class FunctorThr
{
	public:
		void operator()()
		{

			for (int i=0;i<10000;++i) cout<<"Functor Thread "<<this_thread::get_id()<<"running..."<<endl;
		}
};

int main()
{
	cout<<"Spwaning 12 threads..."<<endl;
	vector<thread> threads;
	for (int i=0;i<12;++i)
	{
		threads.push_back(thread( [] {for (int i=0;i<1000;++i) cout<<"Lambda Function Thread "<<this_thread::get_id()<<" running..."<<endl;} ) );
	}


	cout<<"Joining 12 threads..."<<endl;
	for_each(threads.begin(), threads.end(), mem_fn(&thread::join));

	cout<<"Spwaning 12 detached threads..."<<endl;
	for (int i=0;i<12;++i)
	{
		threads.push_back(thread( [] {for (int i=0;i<1000;++i) cout<<"Detached Lambda Function Thread "<<this_thread::get_id()<<" running..."<<endl;} ) );
	}

	cout<<"Detaching 12 threads..."<<endl;
	for_each(threads.begin(), threads.end(), [] (thread &t) {if (t.joinable()) {t.detach();} } );

	return 0;
}
