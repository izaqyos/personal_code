#include <condition_variable>
#include <mutex>

using namespace std;

class FooBar {
private:
    int n;

public:
    FooBar(int n) {
        this->n = n;
        state = true;
    }

    void foo(function<void()> printFoo) {
        
        cond1.notify_all(); //like sem_init to 1 for foo to enter
        state = true; // foo's turn
        for (int i = 0; i < n; i++) {
            
        	// printFoo() outputs "foo". Do not change or remove this line.
            {
              unique_lock<mutex> lock(mtx2);
              cond1.wait(lock, [this] {return this->state;});
        	printFoo();
            state = false;
                cond2.notify_all();
            }
        }
    }

    void bar(function<void()> printBar) {
        cond1.notify_all(); //like sem_init to 1 for foo to enter
        for (int i = 0; i < n; i++) {
            
            {
              unique_lock<mutex> lock(mtx1);
              cond2.wait(lock, [this] {return ! this->state;});
            }
            {
        	// printBar() outputs "bar". Do not change or remove this line.
        	printBar();
            state = true; // foo's turn
            cond1.notify_all();
            }
        }
    }

private:
    mutex: mtx1;
    condition_variable cond1;
    mutex: mtx2;
    condition_variable cond2;
    bool state;

};
