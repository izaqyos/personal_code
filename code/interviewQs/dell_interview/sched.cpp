#include "Task.h"
#include "sched.h"
#include "MTPrinter.h"

#include <string>
#include <thread> //thread
#include <functional> // std::bind
#include <iostream>

using namespace std; 

Sched::Sched(const string &name):
        BaseSched(name)
{
        MTPrint{}<<"Sched CTOR"<<endl;
        m_Thr = thread ( &Sched::schedThread, this) ; //init the scheduler thread 
        sem_init(& m_sem, 0 , 0);
}

const string& Sched::toString() const
{
    return m_sName;
}

void Sched::schedule(BaseTask * pT) //producer, API to push tasks into Q
{
        MTPrint{}<<"Sched::schedule() called"<<endl;
        if (pT == nullptr)
        {
                MTPrint{}<<"Sched::schedule called with an invalid task "<<endl;
                return;
        }

        MTPrint{}<<"Sched::schedule called to schedule task "<<(*pT)<<endl;
        m_mtx.lock();
        m_tasksQ.push(pT);
        m_mtx.unlock();
        sem_post(&m_sem); //sempaphore ++

        MTPrint{}<<"Sched::schedule() task successfuly pushed to tasks Q"<<endl;
        return;
}


void Sched::schedThread() //consumer. pop task from Q and execute it
{
        MTPrint{}<<"Sched::schedThread() initilizing execute thread"<<endl;
        BaseTask * pT = nullptr;
        while (true)
        {

                MTPrint{}<<"Sched::schedThread() , waiting on semaphore (note. this will block until tasks are added to Q)"<<endl;
                sem_wait(&m_sem); // wait for producer to put tasks to Q (thus incrementing semaphore)
                if (! m_tasksQ.empty())
                {
                   m_mtx.lock();
                   pT = m_tasksQ.front();
                   m_tasksQ.pop();
                   m_mtx.unlock();

                   if (pT) 
                   {
                       MTPrint{}<<"Sched::schedThread() running task "<<*(pT)<<endl;
                       pT->execute();
                   }
                }
        }

}


ostream & operator<<(ostream & inpOS, const Sched & sched)
{
    return inpOS<<sched.toString();
}


/*
void Sched::processTasks() //consumer. pop task from Q and execute it
{
        MTPrint{}<<"Sched::processTasks() processing tasks in Q"<<endl;
        BaseTask * pT;
        if (m_bRun.load())
        {
            MTPrint{}<<"Sched::processTasks() run thread is set"<<endl;
                while (! m_tasksQ.empty())
                {
                        pT = m_tasksQ.front();
                        MTPrint{}<<"Sched::processTasks() running task "<<*(pT)<<endl;

                        if (pT) 
                        {
                                pT->execute();
                        }
                        m_mtx.lock();
                        m_tasksQ.pop();
                        m_mtx.unlock();
                }
        }
        //here m_tasks is empty
        m_bRun.store( false);
}

std::atomic<bool> & Sched::shouldRun()
{
        return m_bRun;
}
*/
