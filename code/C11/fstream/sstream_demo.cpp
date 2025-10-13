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
[yizaq@YIZAQ-M-W1ZV:Sat Aug 19:~/Desktop/Work/code/C11/fstream:]$ clang++ -std=c++11 sstream_demo.cpp  -o sstream_demo
[yizaq@YIZAQ-M-W1ZV:Sat Aug 19:~/Desktop/Work/code/C11/fstream:]$ ./sstream_demo 
enter str: 
hello sstream
Got str: hello sstream. Num: 0.5[yizaq@YIZAQ-M-W1ZV:Sat Aug 19:~/Desktop/Work/code/C11/fstream:]$
  */
