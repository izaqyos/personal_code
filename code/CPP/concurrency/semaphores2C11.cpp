#include <thread>
#include <semaphore> //no such header :(
#include <iostream>

using namespace std;

class MySema {

    public:
        //sem_init
    MySema(unsigned int count=0):
    count(count) {
    }

    inline void post() {
        unique_lock<mutex> lock(mutx);
        count++;
        cout<<"thread "<<this_thread::get_id()<<" did sem_post"<<endl;
        cond.notify_all();
    }

    inline void wait( ){
        unique_lock<mutex> lock(mutx);
        while (count == 0 ) {
            cout<<"thread "<<this_thread::get_id()<<" trying sem_wait"<<endl;
            cond.wait(lock);
            cout<<"thread "<<this_thread::get_id()<<" passed sem_wait"<<endl;
        } 
        count--;
    }

    private:
        std::mutex mutx;
        condition_variable cond;
        unsigned int count;

};

unsigned int product =0;
unsigned int times =10;

void produce() {
    for (size_t i = 0; i < times; i++)
    {
        product++;
    }
}

void consume() {
    for (size_t i = 0; i < times; i++)
    {
        cout<<"Consume got "<<product<<endl;
    }
}

MySema getsema(0); //consumer must wait for 1st post
MySema putsema(1); //producer free to produce 1 unit
void produce_sem() {
    for (size_t i = 0; i < times; i++)
    {
        putsema.wait();
        product++;
        getsema.post();
    }
}

void consume_sem() {
    for (size_t i = 0; i < times; i++)
    {
        getsema.wait();
        cout<<"Consume got "<<product<<endl;
        putsema.post();
    }
}

int main() {
    cout<<"No semaphore producer consumer. note the race condition :)"<<endl;
    thread t1(produce);
    thread t2(consume);

    t1.join();
    t2.join();

    cout<<"semaphore producer consumer. note no race condition :)"<<endl;
    thread t3(produce_sem);
    thread t4(consume_sem);

    t3.join();
    t4.join();

}