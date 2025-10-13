#include <iostream>

using namespace std;

void foo(const char word[10] )
{

        cout<<"foo: "<<word<<", of size= "<<sizeof(word)<<endl;
}

int main()
{
const char * ptr1 = 0;
const char * ptr2 = new char[4];
const char * ptr3 = "012345678"; 
char ptr4[10] = "012345678" ;
char ptr5[5] = "0123" ;

cout<<"run foo(ptr1) will crash"<<endl;
//foo(ptr1);
cout<<"about to run foo(ptr2) "<<endl;
foo(ptr2);
cout<<"about to run foo(ptr3) "<<endl;
foo(ptr3);
cout<<"about to run foo(ptr4) "<<endl;
foo(ptr4);
cout<<"about to run foo(ptr5) "<<endl;
foo(ptr5);

}
