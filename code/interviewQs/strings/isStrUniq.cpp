/*
 * =====================================================================================
 *
 *       Filename:  isStrUniq.cpp
 *
 *    Description:  Implement an algorithm to determine if a string has all unique characters What if you can not use additional data structures?
 *
 *        Version:  1.0
 *        Created:  04/07/16 21:41:00
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  YOSI IZAQ
 *   Organization:  
 *
 * =====================================================================================
 */
#include <iostream>
#include <string>

using namespace std;

bool isUniq(const string & str)
{
	long seenMask = 0;
	bool isUnique = true;

	for (int i = 0; i < str.length(); i++) {
		if ( seenMask & ( 1 << ( str[i] - 'a') ) ) 
		{
			isUnique = false;
			break;
		}
		else seenMask |= ( 1 << ( str[i] - 'a') );
	}
	return isUnique;
}

int main()
{
	string sInp;
	cout<<"Enter string\n";
	cin>>sInp;
	cout<<"Check whether string "<<sInp<<" is made of uniq chars\n";
	cout<<"string "<<sInp<<" is "<<(isUniq(sInp) ? "made of uniq chars" : "not made of uniq chars" ) <<"\n";  
	
}

