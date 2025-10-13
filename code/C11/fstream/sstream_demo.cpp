#include <iostream>
#include <sstream>
#include <string>

using namespace std;

int main() {
	stringstream ss;
	string s;
	ss<<"Got str: ";
	cout<<"enter str: "<<endl;
	
	getline(cin, s);
	ss<<s;
	ss<<". Num: "<<0.5;
	cout<<ss.str();
	
	return 0;
}
/*
$ clang++ -std=c++11 sstream_demo.cpp  -o sstream_demo
$ ./sstream_demo 
enter str: 
hello sstream
Got str: hello sstream. Num: 0.5$
  */
