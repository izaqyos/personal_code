/*
 * =====================================================================================
 *
 *       Filename:  LinkedListTester.cpp
 *
 *    Description:  Test linked list, solve riddles
 *
 *        Version:  1.0
 *        Created:  04/13/16 17:34:54
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  YOSI IZAQ
 *   Organization:  
 *
 * =====================================================================================
 */

#include "LinkedList.h"
#include <iostream>

void testLinkedListBasics()
{
	LinkedList<int> lli;

	std::cout <<"testLinkedListBasics() - test adding elements...\n";

	lli.addElem(1);
	lli.addElem(2);
	lli.addElem(3);
	lli.addElem(4);
	lli.addElem(5);
	lli.printMe();

	std::cout <<"testLinkedListBasics() - test remove head\n";
	lli.remElem(5);
	lli.printMe();

	std::cout <<"testLinkedListBasics() - test remove tail\n";
	lli.remElem(1);
	lli.printMe();
}

int main()
{

	int iRet = 0;
	testLinkedListBasics();

	return iRet;
}
