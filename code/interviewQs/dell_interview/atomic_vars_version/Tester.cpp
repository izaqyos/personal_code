#include "Task.h"
#include "sched.h"
#include "MTPrinter.h"

#include <string>
#include <thread>
#include <iostream>

using namespace std; 

static const int NUM_THREADS=2;

void threadf1(string sThrName, int numTasks, BaseTask * task, BaseSched * sched)
{
        MTPrint{}<<"Adding "<<numTasks<<" tasks "<<(*task)<<" to scheduler "<<*(dynamic_cast<Sched *>  (sched) )<<endl;
        if (task == nullptr) 
        {
                MTPrint{}<<"Got null task"<<endl;
                return;
        }

        if (sched == nullptr) 
        {
                MTPrint{}<<"Got null sched"<<endl;
                return;
        }

        for(int i=0;i<numTasks;++i)
        {
                MTPrint{}<<"Thread "<<sThrName<<", id= "<<this_thread::get_id()<<", scheduling task "<<(*task)<<endl;
                sched->schedule(task);
        }
}

int main()
{
        MTPrint{}<<"Start main thread"<<endl;

        Task1 t1("Test Task 1");
        Task2 t2("Test Task 2");
        Sched sched("The scheduler");

        thread threads[2*NUM_THREADS];
        for (int i=0; i<NUM_THREADS; ++i)
        {
                MTPrint{}<<"Main() starting thread "<<i<<endl;
                threads[i] = std::thread(threadf1, "a worker thread", 2, &t1,   &sched);
        }
        for (int i=NUM_THREADS; i<2*NUM_THREADS; ++i)
        {
                MTPrint{}<<"Main() starting thread "<<i<<endl;
                threads[i] = std::thread(threadf1, "a worker thread", 2, &t2,   &sched);
        }

        for (int i=0; i<NUM_THREADS; ++i)
        {
                MTPrint{}<<"Main() joining thread "<<i<<endl;
                threads[i].join();
        }
        for (int i=NUM_THREADS; i<2*NUM_THREADS; ++i)
        {
                MTPrint{}<<"Main() joining thread "<<i<<endl;
                threads[i].join();
        }
}

