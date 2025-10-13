#include <iostream>
#include <string>
#include <vector>

using namespace std;

struct ring_buffer
{
    ring_buffer( std::size_t cap ) : buffer(cap) {}
    bool empty() const { return sz == 0 ; }
    bool full() const { return sz == buffer.size() ; }

    void push( std::string str )
    {
        cout<<"About to push str="<<str<<", first= "<<first<<", last= "<<last<<", sz= "<<sz<<endl;
        if( last >= buffer.size() ) last = 0 ;
        buffer[last] = str ;
        ++last ;
        if( full() ) first = (first+1) %  buffer.size() ;
        else ++sz ;
    }

    void pop()
    {
        cout<<"About to pop "<<", first= "<<first<<", last= "<<last<<", sz= "<<sz<<endl;
        if (sz > 0) sz--;
        else return;

        if (last > 0) last--;
        else last = buffer.size()-1;
        cout<<"last: "<<last<<endl;
    }

    std::string& operator[] ( std::size_t pos )
    {
        auto p = ( first + pos ) % buffer.size() ;
        cout<<"[] operator"<<", first= "<<first<<", last= "<<last<<", sz= "<<sz<<", pos="<<pos<<" index="<< p<<endl;
        return buffer[p] ;
    }

    std::ostream& print( std::ostream& stm = std::cout ) const
    {
        cout<<"print: "<<", first= "<<first<<", last= "<<last<<", sz= "<<sz<<endl;
        if( first < last )
            for( std::size_t i = first ; i < last ; ++i ) std::cout << buffer[i] << ' ' ;
        else
        {
            for( std::size_t i = first ; i < buffer.size() ; ++i ) std::cout << buffer[i] << ' ' ;
            for( std::size_t i = 0 ; i < last ; ++i ) std::cout << buffer[i] << ' ' ;
        }
        return stm ;
    }

    private:
        std::vector<std::string> buffer ;
        std::size_t first = 0 ;
        std::size_t last = 0 ;
        std::size_t sz = 0 ;
};

int main()
{
    ring_buffer rb(8) ;

    for( int i = 10 ; i < 30 ; ++i )
    {
        rb.push( std::to_string(i) ) ;
        rb.print() << '\n' ;
    }

    for  (int i=0; i<10; ++i) 
    {
            rb.pop();
        rb.print() << '\n' ;
    }
}


/*
 *
Tests:
[212680136@G9VK2GH2E:2018-02-06 15:17:34:/cygdrive/c/Users/212680136/Desktop/Yosi/Work/code/CPP/data_structures:]2007$ g++ -std=c++0x ring_buffer.cpp -o ring_buffer 
[212680136@G9VK2GH2E:2018-02-06 15:18:14:/cygdrive/c/Users/212680136/Desktop/Yosi/Work/code/CPP/data_structures:]2007$ ./ring_buffer.exe  
About to push str=10, first= 0, last= 0, sz= 0
print: , first= 0, last= 1, sz= 1
10 
About to push str=11, first= 0, last= 1, sz= 1
print: , first= 0, last= 2, sz= 2
10 11 
About to push str=12, first= 0, last= 2, sz= 2
print: , first= 0, last= 3, sz= 3
10 11 12 
About to push str=13, first= 0, last= 3, sz= 3
print: , first= 0, last= 4, sz= 4
10 11 12 13 
About to push str=14, first= 0, last= 4, sz= 4
print: , first= 0, last= 5, sz= 5
10 11 12 13 14 
About to push str=15, first= 0, last= 5, sz= 5
print: , first= 0, last= 6, sz= 6
10 11 12 13 14 15 
About to push str=16, first= 0, last= 6, sz= 6
print: , first= 0, last= 7, sz= 7
10 11 12 13 14 15 16 
About to push str=17, first= 0, last= 7, sz= 7
print: , first= 0, last= 8, sz= 8
10 11 12 13 14 15 16 17 
About to push str=18, first= 0, last= 8, sz= 8
print: , first= 1, last= 1, sz= 8
11 12 13 14 15 16 17 18 
About to push str=19, first= 1, last= 1, sz= 8
print: , first= 2, last= 2, sz= 8
12 13 14 15 16 17 18 19 
About to push str=20, first= 2, last= 2, sz= 8
print: , first= 3, last= 3, sz= 8
13 14 15 16 17 18 19 20 
About to push str=21, first= 3, last= 3, sz= 8
print: , first= 4, last= 4, sz= 8
14 15 16 17 18 19 20 21 
About to push str=22, first= 4, last= 4, sz= 8
print: , first= 5, last= 5, sz= 8
15 16 17 18 19 20 21 22 
About to push str=23, first= 5, last= 5, sz= 8
print: , first= 6, last= 6, sz= 8
16 17 18 19 20 21 22 23 
About to push str=24, first= 6, last= 6, sz= 8
print: , first= 7, last= 7, sz= 8
17 18 19 20 21 22 23 24 
About to push str=25, first= 7, last= 7, sz= 8
print: , first= 0, last= 8, sz= 8
18 19 20 21 22 23 24 25 
About to push str=26, first= 0, last= 8, sz= 8
print: , first= 1, last= 1, sz= 8
19 20 21 22 23 24 25 26 
About to push str=27, first= 1, last= 1, sz= 8
print: , first= 2, last= 2, sz= 8
20 21 22 23 24 25 26 27 
About to push str=28, first= 2, last= 2, sz= 8
print: , first= 3, last= 3, sz= 8
21 22 23 24 25 26 27 28 
About to push str=29, first= 3, last= 3, sz= 8
print: , first= 4, last= 4, sz= 8
22 23 24 25 26 27 28 29 
About to pop , first= 4, last= 4, sz= 8
last: 3
print: , first= 4, last= 3, sz= 7
22 23 24 25 26 27 28 
About to pop , first= 4, last= 3, sz= 7
last: 2
print: , first= 4, last= 2, sz= 6
22 23 24 25 26 27 
About to pop , first= 4, last= 2, sz= 6
last: 1
print: , first= 4, last= 1, sz= 5
22 23 24 25 26 
About to pop , first= 4, last= 1, sz= 5
last: 0
print: , first= 4, last= 0, sz= 4
22 23 24 25 
About to pop , first= 4, last= 0, sz= 4
last: 7
print: , first= 4, last= 7, sz= 3
22 23 24 
About to pop , first= 4, last= 7, sz= 3
last: 6
print: , first= 4, last= 6, sz= 2
22 23 
About to pop , first= 4, last= 6, sz= 2
last: 5
print: , first= 4, last= 5, sz= 1
22 
About to pop , first= 4, last= 5, sz= 1
last: 4
print: , first= 4, last= 4, sz= 0
22 23 24 25 26 27 28 29 
About to pop , first= 4, last= 4, sz= 0
print: , first= 4, last= 4, sz= 0
22 23 24 25 26 27 28 29 
About to pop , first= 4, last= 4, sz= 0
print: , first= 4, last= 4, sz= 0
22 23 24 25 26 27 28 29 

 *
 */
