/*
 * =====================================================================================
 *
 *       Filename:  threadsRaceCond.cpp
 *
 *    Description:  how to pass params to a thread, and race cond. demo + fix
clang++ -std=c++11 threadsRaceCond.cpp  -o threadsRaceCond
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
#include <string>
#include <algorithm> //for_each
#include <functional> //mem_fn (calls member function of input class instance by creating a wrapper...

using namespace std;

void thrPassByValueFunc(int x, string s)
{
	for (int i=0;i<x;++i) cout<<"Thread "<<this_thread::get_id()<<" output("<<x<<"): "<<s<<endl;
}


void thrPassByRefFunc(const int &x)
{
	int & y = const_cast<int &>(x);
	++y;

	for (int i=0;i<x;++i) cout<<"Thread "<<this_thread::get_id()<<" output("<<x<<"): "<<endl;
}

class foo
{
	public:
		/*
	foo(){}

	foo(const foo & ins){}
  */
	void bar(int x)
	{
		cout<<"Inside Foo::bar() method invoked w/ argument: "<<x<<endl;
	}
};

class RCDemo
{
	int treasure;
	public:
	RCDemo():
		treasure(0)
	{}

	int getTreasure(){return treasure;}

	void addTreasure(int gold)
	{
		cout<<"adding "<<gold<<endl;
		for(int i=0; i<gold;++i)
		{
			cout<<"incr 1";
			treasure++; //increment one at a time to demo race condition...
		}
	}
};

int testRaceCond()
{

	RCDemo rcdemo;
	vector<thread> dwarves;
	for(int i=0; i<5; ++i)
		dwarves.push_back(thread(&RCDemo::addTreasure, rcdemo, 1000));

	for_each(dwarves.begin(), dwarves.end(), mem_fn(&thread::join));

	cout<<"sum: "<<rcdemo.getTreasure()<<endl;
	return rcdemo.getTreasure();
}

int main()
{
	cout<<"Demo of a. passing values to threads and b. passing ptr to class method+arguments and c. race condition..."<<endl;

	int x=1;
	thread PbV_Thr( thrPassByValueFunc, x, "passed string"  );
	PbV_Thr.join();

	cout<<"X val before trigger pass-by-ref thread: "<<x<<endl;
	thread PbR_Thr(thrPassByRefFunc, ref(x));
	PbR_Thr.join();
	cout<<"X val after trigger pass-by-ref thread: "<<x<<endl;

	cout<<"b. passing ptr to class method+arguments "<<endl;
	foo f;
	thread PCMFPtrThr(&foo::bar, &f,x); //PassClassMethodFuncPtrThread...
	PCMFPtrThr.join();

	cout<<"c. let the races begin :) - each test will be creating five dwarven threads to mine gold. each will mine 1000 gold coins. Run 5k tests and check sum is as expected"<<endl;
	int res = 0;
	for (int i=0; i<5000;++i)
	{
		if ((res=testRaceCond()) != 5000)
			cout<<"Test case "<<i<<" resulted in unexpected sum "<<res<<" when 5000 was expected"<<endl;
	}

	return 0;
}
