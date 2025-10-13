/*
 * =====================================================================================
 *
 *       Filename:  my_stack.cpp
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  07/07/15 19:01:22
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  YOSI IZAQ
 *   Organization:  
 *
 * =====================================================================================
 */
#include <stdlib.h>

#include <iostream>
#include <exception>
#include <string>

using namespace std;

class StackEmpty : public exception
{
	virtual const char * what() const throw()
	{
		return "Stack Empty exception has occured ";
	}
}

class StackFull : public exception
{
	virtual const char * what() const throw()
	{
		return "Stack Full exception has occured ";
	}
}

template <typename E>
class myStack
{
	public:
	myStack();
	virtual ~myStack();

	private:
	virtual void push (E &) =0;
	virtual void pop () throw(StackEmpty) =0;
	virtual unsigned int size() const =0;
	virtual bool empty() const =0;
	virtual const E & top() const throw(StackEmpty) =0;
}

template <typename E>
class myArrStack : public myStack 
{
	public:
	myArrStack( unsigned int iSize = 100);
	virtual ~myArrStack();

	private:
	virtual void push (E &) throw(StackFull) ;
	virtual void pop () throw(StackEmpty) ;
	virtual unsigned int size() const ;
	virtual bool empty() const ;
	virtual const E & top() const throw(StackEmpty) ;
	unsigned int iCap ; // Stack capacity
	int iTop ; // Stack top index
	E * pStackArr ; 
}

template <typename E>
myArrStack::myArrStack(unsigned int iSize ):
	iCap(iSize), iTop(-1), pStackArr(new E[iSize])
{

}

template <typename E>
myArrStack::~myArrStack()
{
	delete pStackArr ;
	pStackArr = NULL;
	iTop = -1;
}

template <typename E>
void myArrStack::push (E &) 
{

}
