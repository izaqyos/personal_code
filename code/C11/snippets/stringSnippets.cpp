/*
 * =====================================================================================
 *
 *       Filename:  stringSnippets.cpp
 *
 *    Description:  Snippets of strings operations
 *
 *        Version:  1.0
 *        Created:  04/13/2017 14:17:05
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Yosi Izaq
 *   Organization:  
 *
 * =====================================================================================
 */
#include <iostream>
#include <string>
#include <vector>

using namespace std;

string sayNum(string str)
{
	//Get a str representing a number say 1211 ans "say" it. 
	// e.g. return 111221 (as in one 1, one 2, two 1)
	string ret;

	char lastSeen,c;
	unsigned int rep = 0;
	for (int i=0; i<str.length();++i)
	{
		c=str[i];
		if(i == 0) 
		{
			lastSeen = c;
		}

		if (c==lastSeen)
		{
			rep++;
		}
		else
		{
			ret+= to_string(rep) + lastSeen ;
			rep=1;
			lastSeen = c;
		}
		cout<<"sayNum(): c: "<<c<<", last: "<<lastSeen<<", rep: "<<rep<<", ret="<<ret<<endl;
	}

	ret+= to_string(rep) + lastSeen +", ";
	return ret;


}
int main(int argc, char *argv[])
{

	string testStr="1, 11, 21, 1211, 111221,";
	cout<<"testStr: "<<testStr<<endl;

	string lastField(testStr.substr(0, testStr.length()-1));
	cout<<"lastField after peeling last ,: "<<lastField<<endl;
	lastField = lastField.substr(lastField.find_last_of(',', string::npos));
	cout<<"lastField: "<<lastField<<endl;


	vector<string> vInputs = {"1", "11", "21", "1211", "111221"};
	for_each(vInputs.begin(), vInputs.end(), [] (string s){ cout<<"say num "<<s<<" -> "<<sayNum(s)<<endl;});

	return 0;
}
