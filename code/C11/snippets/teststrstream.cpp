#include <iostream>
#include <sstream>

using namespace std;

int main()
{
stringstream ss;
ss<<"aaa";
cout<<ss.str()<<endl;
ss<<"oops, sstream concats data";
cout<<ss.str()<<endl;

ss.clear();
ss<<"oops clear, just clears error flags, not content";
cout<<ss.str()<<endl;

ss.str("");
ss<<"one way to clear, call str(\"\")";
cout<<ss.str()<<endl;

}
