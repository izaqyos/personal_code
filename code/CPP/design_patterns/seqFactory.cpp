/*
 * =====================================================================================
 *
 *       Filename:  seqFactory.cpp
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  08/14/16 21:09:25
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  YOUR NAME (), 
 *   Organization:  
 *
 * =====================================================================================
 */
#include "stdSeq.h"
#include <iostream>
#include <string>

using namespace std;

template <typename T>
class seqFactory
{

	public:
		static aSequence<T> * newSeq(const string & sType)
		{
			if (sType == "list") return new aList<T>(sType);
			if (sType == "deque") return new aDeque<T>(sType);
			return NULL;
		}

};

int main()
{
	aSequence<int> * pIntList  = seqFactory<int>::newSeq("list");
	pIntList->printMe();
}
