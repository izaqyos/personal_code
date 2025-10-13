/*
 * =====================================================================================
 *
 *       Filename:  regexp.cpp
 *
 *    Description:  
 *  email: I’m thinking of putting in place a simple workaround. 
 *  email: Check for offending user name (regexp:  .*@.*\.\..* Or .*@.*\.$) ; if match make ISE drop the auth. 
 *  email: I plan to put the check and set auth res. To drop in AD ID store.*
 *        Version:  1.0
 *        Created:  02/24/2014 10:41:12
 *       Revision:  none
 *       Compiler:  gcc
 *       [yizaq@yizaq-mac:Mon Feb 24:~/Desktop/Work/code/CPP/tests/string:]$ g++ -L/usr/local/Cellar/boost/1.55.0/lib -lboost_regex-mt -lboost_filesystem-mt -lboost_thread-mt    regexp.cpp 
 *
 *         Author:  Yosi Izaq
 *   Organization:  
 *
 * =====================================================================================
 */
#include <stdlib.h>
#include <stdio.h>
#include <string>
#include <iostream>
#include <boost/regex.hpp>

using namespace std;
using namespace boost;

bool str_match_patterns(const string & s_inp) 
{

	size_t pos = s_inp.find_first_of("@");
	if (pos != string::npos)
	{
		size_t pos1 = s_inp.find_first_of(".", pos);
	        if (pos1 != string::npos)
		{
			if ( (s_inp[pos1+1] == '.') ) 
			{
				cout<<"String "<<s_inp<<" matches disallowed pattern a@b..c "<<endl;
				return true;
			}
		        size_t pos2 = s_inp.find_first_of(".", pos1+1);
			//cout<<"pos1 "<<pos1 <<" pos2 "<<pos2 << endl;
			if ( (pos2 != string::npos) && (s_inp[pos2+1] == s_inp[s_inp.length()]) )
			{

				cout<<"String "<<s_inp<<" matches disallowed pattern a@b.c. "<<endl;
				return true;
			}
		}
	}
	return false;
}

int main(int argc, const char *argv[])
{
	string inp1 = "yosi@cisco..com";	
	string inp2 = "yosi@cisco.com.";	
	string inp3 = "";	

	const regex re1(  ".*\\@.*\\.\\..*" );
	const regex re2(  ".*\\@.*\\.$" );

	cout<<"Please enter pattern"<<endl;
	cin>>inp3;
	cout<<"You entered pattern "<<inp3<<endl;

	if (regex_match(inp1,re1)) {
	    cout<<inp1<<" boost regex match pattern 1"<<endl;
	}
	else {
	    cout<<inp1<<" does not boost regex match pattern 1"<<endl;
		
	}
	if (regex_match(inp1,re2)) {
	    cout<<inp1<<" boost regex match pattern 2"<<endl;
	}
	else {
	    cout<<inp1<<" does not boost regex match pattern 2"<<endl;
		
	}

	if (regex_match(inp2,re1)) {
	    cout<<inp2<<" boost regex match pattern 1"<<endl;
	}
	else {
	    cout<<inp2<<" does not boost regex match pattern 1"<<endl;
		
	}
	if (regex_match(inp2,re2)) {
	    cout<<inp2<<" boost regex match pattern 2"<<endl;
	}
	else {
	    cout<<inp2<<" does not boost regex match pattern 2"<<endl;
		
	}

	if (regex_match(inp3,re1)) {
	    cout<<inp3<<" boost regex match pattern 1"<<endl;
	}
	else {
	    cout<<inp3<<" does not boost regex match pattern 1"<<endl;
		
	}
	if (regex_match(inp3,re2)) {
	    cout<<inp3<<" boost regex match pattern 2"<<endl;
	}
	else {
	    cout<<inp3<<" does not boost regex match pattern 2"<<endl;
		
	}

	if (str_match_patterns(inp1)) {
	    cout<<inp1<<" string match pattern "<<endl;
	}
	else {
	    cout<<inp1<<" does not string match pattern "<<endl;
		
	}
	if (str_match_patterns(inp2)) {
	    cout<<inp2<<" string match pattern "<<endl;
	}
	else {
	    cout<<inp2<<" does not string match pattern "<<endl;
		
	}
	if (str_match_patterns(inp3)) {
	    cout<<inp3<<" string match pattern "<<endl;
	}
	else {
	    cout<<inp3<<" does not string match pattern "<<endl;
		
	}

	return 0;
}
