class Foo {
public:
    Foo() {
      state = 0;
    }

    void  first(function<void()> printFirst) {
        
        
        // printFirst() outputs "first". Do not change or remove this line.
        thread::id tid = this_thread::get_id();
        cout<<"First thread, id="<<tid;
        printFirst();
        state = 1;
        cond.notify_all();
    }

    void   second(function<void()> printSecond) {
        unique_lock<mutex> lock(mtx);
        //while (state !=1 ) cond.wait(lock); //c way
        cond.wait(lock, [this] {return this->state == 1;});
        // printSecond() outputs "second". Do not change or remove this line.
        thread::id tid = this_thread::get_id();
        cout<<"Seconde thread, id="<<tid;
        printSecond();
        state = 2; 
        cond.notify_all();
    }

    void  third(function<void()> printThird) {
        unique_lock<mutex> lock(mtx);
        // while (state !=2 ) cond.wait(lock); 
        cond.wait(lock, [this] {return this->state == 2;});
        
        // printThird() outputs "third". Do not change or remove this line.
        thread::id tid = this_thread::get_id();
        cout<<"Third thread, id="<<tid;
        printThird();
        state = 0;
    }

    private:
       unsigned int state;
       mutex mtx;
       condition_variable cond;
};
