/*
 * =====================================================================================
 *
 *       Filename:  genStrPermutations.cpp
 *
 *    Description:  Generate all input string permutations in lexicographic order
 *
 *        Version:  1.0
 *        Created:  01/08/17 20:50:43
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  YOSI IZAQ
 *   Organization:  
[yizaq@YIZAQ-M-W1ZV:Sun Jan 08:~/Desktop/Work/code/interviewQs/gen_permutations:]$ clang++ -std=c++11 genStrPermutations.cpp -o genStrPermutations
 *
 * =====================================================================================
 */
#include <string>
#include <iostream>
#include <algorithm>

using namespace std;


void genPerms(string selected, string remainder)
{
	//cout<<"selected: "<<selected<<", remainder: "<<remainder<<endl;
	if (remainder.empty()) //stop condition - remainder empty
	{
		cout<<selected<<endl;
		return;

	}
	else
	{
		for(int i=0; i<remainder.length(); ++i)
		{
			string rem_copy = remainder;
			genPerms(selected+remainder[i], rem_copy.erase(i,1));
		}
	}
}

int main()
{
	string str;
	cout<<"please enter input string"<<endl;
	cin>>str;

	cout<<"Generate all permutations of "<<str<<endl;

	sort(str.begin(), str.end());
	genPerms("",str);
	
	
}

