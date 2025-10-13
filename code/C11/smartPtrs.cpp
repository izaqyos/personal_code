/*
 * =====================================================================================
 *
 *       Filename:  smartPtrs.cpp
 *
 *    Description:  :Demo smart C11 pointers
 *
 *        Version:  1.0
 *        Created:  01/04/15 16:02:48
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  YOSI IZAQ
 *   Organization:  
 *
 * =====================================================================================
 */
#include <stdlib.h>
#include <stdio.h>
#include <map>
#include <vector>
#include <string>
#include <iostream>
#include <memory>
#include <thread>
#include <chrono>
#include <mutex>
 
struct Base
{
    Base() { std::cout << "  Base::Base()\n"; }
    // Note: non-virtual destructor is OK here
    ~Base() { std::cout << "  Base::~Base()\n"; }
};
struct Derived: public Base
{
    Derived() { std::cout << "  Derived::Derived()\n"; }
    ~Derived() { std::cout << "  Derived::~Derived()\n"; }
};
 
void thr(std::shared_ptr<Base> p)
{
    std::this_thread::sleep_for(std::chrono::seconds(1));
    std::shared_ptr<Base> lp = p; // thread-safe, even though the
                                  // shared use_count is incremented
    {
      static std::mutex io_mutex;
      std::lock_guard<std::mutex> lk(io_mutex);
      std::cout << "local pointer in a thread:\n"
                << "  lp.get() = " << lp.get()
                << ", lp.use_count() = " << lp.use_count() << '\n';
    }
}
 
class B 
{
	public:
		   virtual void f(int) {std::cout << "B::f" << std::endl;}
};

using namespace std;

class D : public B
{
	public:
		   virtual void f(int) override final {std::cout << "D::f" << std::endl;}
};

//class F : public D
//{
//	public:
//		   virtual void f(int) override {std::cout << "F::f" << std::endl;}
//		   // Produces error :smartPtrs.cpp:42:19: error: declaration of 'f' overrides a 'final' function virtual void f(int) override {std::cout << "F::f" << std::endl;}
//};

enum class Options {None, One, All}; // scoped enum aka class enum
int main()
{
auto o = Options::All;
cout<<"Print scoped enum value: "<< static_cast<int>(o)<<endl; 

unique_ptr<int> iP;
iP.reset( new int{5}) ; // new universal initialization syntax
cout<<"Created unique_ptr to int, used reset to copy raw ptr: "<< *iP<<endl; 

auto iP2 = move(iP);
cout<<"Moved unique_ptr ownership, value: "<< *iP2<<endl; 

//"Custome delete function " 
auto delInt = [] (int * ip) {
	cout <<"Custome delete function called "<<endl;
	delete ip;
       };
unique_ptr<int, decltype(delInt)> iPD(nullptr, delInt);
iPD.reset( new int{4}) ; // new universal initialization syntax
cout<<"Created unique_ptr to int that has custome delete, value: "<< *iPD<<endl; 

  std::shared_ptr<Base> p = std::make_shared<Derived>();
 
    std::cout << "Created a shared Derived (as a pointer to Base)\n"
              << "  p.get() = " << p.get()
              << ", p.use_count() = " << p.use_count() << '\n';
    std::thread t1(thr, p), t2(thr, p), t3(thr, p);
    p.reset(); // release ownership from main
    std::cout << "Shared ownership between 3 threads and released\n"
              << "ownership from main:\n"
              << "  p.get() = " << p.get()
              << ", p.use_count() = " << p.use_count() << '\n';
    t1.join(); t2.join(); t3.join();
    std::cout << "All threads completed, the last one deleted Derived\n";
}
