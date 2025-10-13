/*
 * =====================================================================================
 *
 *       Filename:  simpleFPthread.cpp
 *
 *    Description:  Simple thread created w pointer to function
clang++ -std=c++11 simpleFPthread.cpp  -o simpleFPthread
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
	thread thr(thrFunc), thr1((FunctorThr())), thr2( [] {for (int i=0;i<10000;++i) cout<<"Lambda Function Thread "<<this_thread::get_id()<<"running..."<<endl;} );

	for (int i=0;i<10000;++i) cout<<"Main Thread running threads:"<<endl;
	cout<<"Thread id: "<<thr.get_id()<<endl;
	cout<<"Thread id: "<<thr1.get_id()<<endl;
	cout<<"Thread id: "<<thr2.get_id()<<endl;

	thr.join();
	thr1.join();
	thr2.join();

	cout<<"main and slave threads complete"<<endl;
	return 0;
}
