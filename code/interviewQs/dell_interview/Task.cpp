#include "Task.h"
#include "MTPrinter.h"
#include <iostream>

//#include <cstdlib> //rand
//#include <ctime> //time
// 
        //srand(time(nullptr)); //seed rand
        //srand(time(nullptr)); //seed rand
        //int sleepT = rand();

#include <random>
#include <chrono> //for time functions
#include <thread> //sleep_for
using namespace std;

Task1::Task1(string  name)
{
        MTPrint{}<<"Task1 CTOR called w/ name "<<name<<endl;
        m_sName = name;
}

void Task1::execute() const
{
        MTPrint{}<<"Task1::execute() called"<<endl;
        random_device rd; // seed rand engine
        mt19937 rng(rd()); // mersenne-twister RNG
        uniform_int_distribution<int> uni(1,10); //uniform distribution guaranteed

        int sleepT = uni(rng);
        MTPrint{}<<"Task1 "<<m_sName<<" performing lots of work ;) sleep for "<<sleepT<<" seconds"<<endl;
        
        this_thread::sleep_for(chrono::milliseconds(sleepT * 1000)); 
        MTPrint{}<<"Task1::execute() complete"<<endl;
}


Task2::Task2(string  name)
{
        MTPrint{}<<"Task2 CTOR called w/ name "<<name<<endl;

        m_sName = name;
}

void Task2::execute() const
{
        MTPrint{}<<"Task2::execute() called"<<endl;

        random_device rd; // seed rand engine
        mt19937 rng(rd()); // mersenne-twister RNG
        uniform_int_distribution<int> uni(1,10); //uniform distribution guaranteed

        int sleepT = uni(rng);
        MTPrint{}<<"Task2 "<<m_sName<<" performing lots of work ;) sleep for "<<sleepT<<" seconds"<<endl;
        
        this_thread::sleep_for(chrono::milliseconds(sleepT * 1000)); 

        MTPrint{}<<"Task2::execute() complete"<<endl;
}

ostream & operator<<(ostream & inpOS, const BaseTask & task)
{
    return inpOS<<task.toString();
}
