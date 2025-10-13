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
}

const string& Sched::toString() const
{
    return m_sName;
}

void Sched::schedule(BaseTask * pT)
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

        MTPrint{}<<"Sched::schedule() task successfuly pushed to tasks Q"<<endl;
        //if (!m_bRun.load())
        if (m_tasksQ.size() == 1) // first task after empty. set run flag
        {
            MTPrint{}<<"Sched::schedule() detected first task"<<endl;
                {
                std::unique_lock<std::mutex> CVLock(m_cvmtx);  
                MTPrint{}<<"Sched::schedule() raising run flag and notifying one thread"<<endl;
                m_bRun.store( true);
                m_CV_ShouldRun.notify_one(); //only one sched runner thread to notify 
                } //since CVLock is a scoped lock here it unlocks. not notify
        }

        return;
}

std::atomic<bool> & Sched::shouldRun()
{
        return m_bRun;
}

void Sched::processTasks()
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
void Sched::schedThread()
{
        MTPrint{}<<"Sched::schedThread() initilizing execute thread"<<endl;
        while (true)
        {

                MTPrint{}<<"Sched::schedThread() load run flag (atomic var)..."<<endl;
                if(!m_bRun.load())
                {
                        MTPrint{}<<"Sched::schedThread() run flag is set"<<endl;
                        {
                                std::unique_lock<std::mutex> CVLovk(m_cvmtx);
                                MTPrint{}<<"Sched::schedThread() waiting for signal to run"<<endl;
                                m_CV_ShouldRun.wait(CVLovk, std::bind(&Sched::shouldRun, this) );
                                processTasks() ;
                        }

                }
                else
                {
                        processTasks();//lock,pop task,unlock, run task. if Q empty set m_bRun to false
                }
        }

}


ostream & operator<<(ostream & inpOS, const Sched & sched)
{
    return inpOS<<sched.toString();
}
