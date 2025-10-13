/*
 * =====================================================================================
 *
 *       Filename:  set.cpp
 *
 *    Description:  play w/ set
 *
 *        Version:  1.0
 *        Created:  02/25/16 12:19:06
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  YOSI IZAQ
 *   Organization:  
 *
 * =====================================================================================
 */
#include <iostream>
#include <set>
#include <string>

using namespace std;

template <typename ContainerT> void printContainer( ContainerT & container)
{

	cout<<"container: {";
	typename ContainerT::const_iterator j= container.begin();
	for (typename ContainerT::const_iterator i = container.begin(); i != container.end(); ++i) {
		
		if ( (++j) != container.end() ) cout<<*i<<",";
		else cout<<*i;
	}
	cout<<"}"<<endl;

	// BTW, to get Container type use ContainerT::value_type 
}

int main ()
{
	int nums[10] = {1,5,6,1,1,5,9,0,6,9};
	set<int> myset(nums, nums+10);
	set<int> myset1; // empty
	set<int> myset2(myset1); // copy ctor


	printContainer<set<int> > (myset);

	if (myset1.empty()) {
		cout<<"myset1 is empty"<<endl;
	}
	cout<<"size of myset "<<myset.size()<<endl;

	myset1.insert(1);
	myset1.insert(1);
	myset1.insert(2);
	myset1.insert(5);
	myset1.insert(3);
	myset1.insert(1);
	myset1.insert(4);
	myset1.insert(4);
	myset1.insert(5);
	myset1.insert(6);

	cout<<"myset1 after inserts: "<<endl;
	printContainer<set<int> > (myset1);

	myset1.erase(3);
	myset1.erase(5);
	cout<<"myset1 after erases: "<<endl;
	printContainer<set<int> > (myset1);
}
