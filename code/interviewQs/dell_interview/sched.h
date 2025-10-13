#ifndef __SCHED__
#define __SCHED__

#include <thread>
#include <queue>
#include <string>
#include <atomic>
#include <mutex>
#include <condition_variable>
#include <semaphore.h>

class BaseTask; //fwd decl

class BaseSched
{
        public:
            virtual void schedule(BaseTask * pT) =0;
            BaseSched(const std::string & name) : m_sName(name) {};
            BaseSched():BaseSched("Default Scheduler"){};


        protected:
            virtual void schedThread() = 0; //code to be run using m_Thr thread, executes all tasks that were registered to scheduler via schedule  
            std::string m_sName = "Some Scheduler";
            std::thread m_Thr; //main scheduler thread
            sem_t m_sem;
};

class Sched: public BaseSched
{
        public:
                Sched( const std::string & name);
                Sched() :BaseSched("Default Scheduler"){};
                void schedule(BaseTask *pT);
                ~Sched(){ m_Thr.join();};

                std::string const & toString() const; 

        protected:
                void schedThread();
                //std::atomic<bool> & shouldRun();
                void processTasks();

        private:
                friend std::ostream& operator<<(std::ostream & inpOS, const Sched & sched);
                std::queue<BaseTask *> m_tasksQ;
                std::mutex m_mtx; //mutex for protecting read/write from/to Q. no need for RW locks since reader also writes (so no RO users) 
                //std::atomic<bool> m_bRun = {false};
                //std::mutex m_cvmtx; //mutex for CV unique_lock 
                //std::unique_lock<std::mutex> m_CVLock; //required for the cond var.
                //std::condition_variable m_CV_ShouldRun;
};

#endif
