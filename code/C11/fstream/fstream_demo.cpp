#include <iostream>
#include <fstream>
using namespace std;

int main() {
	// write to text file
	ofstream ofs("out.txt");
	//ofs.open("out.txt"); //performed by CTOR
	ofs<<"Hello ofstream";
	ofs.close();
	
	ifstream ifs("out.txt");
	string line;
	//ifs.open("out.txt"); //performed by CTOR
	if (ifs.is_open())
	{
		while (getline(ifs,line)) cout<<"Read line: "<<line<<endl;
	}
	streampos begin, end;
	ifs.seekg(0, ios::beg);
	begin = ifs.tellg();
	ifs.seekg(0, ios::end);
	end  = ifs.tellg();
	cout<<"File size: "<<end-begin<<" bytes"<<endl;
	ifs.close();
	return 0;
}
