#include <iostream>
#include <semaphore>
#include <thread>
#include <vector>

using namespace std;

vector<int> workQueue{};

counting_semaphore<1> startWork(0);

void prepWork() {
    workQueue.insert(workQueue.end(), {0,1,0,3});
    cout<<"Producer prepared work unit"<<endl;
    startWork.release(); //increment semaphore
}

void consumeWork() {
    cout<<"Consumer (worker) waiting for work"<<endl;
    startWork.acquire(); //decrement semaphore or block if it's 0 (no work unit in Q)
    workQueue[2] = 2;
    cout<<"Consumer (worker) work done"<<endl;
    for (auto elem: workQueue) {
        cout<<elem;
    }
    cout<<endl;
}

int main(int argc, char const *argv[])
{
    thread t1(prepWork);
    thread t2(consumeWork);
    t1.join();
    t2.join();
    return 0;
}

