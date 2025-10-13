/*
 * =====================================================================================
 *
 *       Filename:  future_101.cpp
 *
 *    Description:  playground for future, async
 *
 *        Version:  1.0
 *        Created:  03/27/2017 21:25:11
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Yosi Izaq
 *   Organization:  
 *
 * =====================================================================================
 */
/*
 * 


yizaq@YIZAQ-M-W1ZV:Mon Mar 27:~/Desktop/Work/code/C11/future:]$ clang++ -std=c++11 future_101.cpp  -o future_101
[yizaq@YIZAQ-M-W1ZV:Mon Mar 27:~/Desktop/Work/code/C11/future:]$ ./future_101 
Hello future
Hello future
Running 4 helloFuture threads via future...
Hello future
Hello future
[yizaq@YIZAQ-M-W1ZV:Mon Mar 27:~/Desktop/Work/code/C11/future:]$ ./future_101 
Hello future
Hello future
Hello future
Hello future
Running 4 helloFuture threads via future...
[yizaq@YIZAQ-M-W1ZV:Mon Mar 27:~/Desktop/Work/code/C11/future:]$ ./future_101 
Hello futureHello future

Hello futureRunning 4 helloFuture threads via future...Hello future


[yizaq@YIZAQ-M-W1ZV:Mon Mar 27:~/Desktop/Work/code/C11/future:]$ ./future_101 
Hello future
Hello future
Hello future
Hello future
Running 4 helloFuture threads via future...
 */
#include <iostream>
#include <vector>
#include <future>

using namespace std;

void helloFuture()
{
	cout<<"Hello future"<<endl;
}

int main()
{

	future<void> res1(async(helloFuture));
	future<void> res2(async(helloFuture));
	future<void> res3(async(helloFuture));
	future<void> res4(async(helloFuture));

	//now w/ lambda func that returns sum
	future<int> res5(async([](int x, int y){return x+y;},2,3));
	future<int> res6(async([](int x, int y){return x+y;},20,3));

	cout<<"Running 4 helloFuture threads via future..."<<endl;

	//if by now helloFuture wasn't called. explicitly call it
	res1.get();
	res2.get();
	res3.get();
	res4.get();
	cout<<"res5: "<<res5.get()<<endl;
	cout<<"res6: "<<res6.get()<<endl;

	//lol, use thread vector 
	vector<future<int>> futures;
	for (int i=0; i<20;++i)
	{
		futures.push_back(async([](int x){return x*x;},i));
	}

	cout<<"Running square 0-19:"<<endl;
	for (int i=0; i<20;++i)
	{
		cout<<"res"<<i<<": "<<futures[i].get()<<endl;
	}
	return 0;

}
