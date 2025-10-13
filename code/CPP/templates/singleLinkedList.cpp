/*
 * =====================================================================================
 *
 *       Filename:  singleLinkedList.cpp
 *
 *    Description: Template single linked list 
 *
 *        Version:  1.0
 *        Created:  06/30/15 15:29:40
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
#include <string>

using namespace std;

template <typename > class SLL;

template <typename T>
class sllNode
{
	private:
		sllNode<T> * next;
		T val;

         friend class SLL<T>;
};

template <typename T>
ostream & operator << (ostream & os, const SLL<T> & obj)
{
	os<<"-----------Printing Single Linked List Content ----------------------"<<endl;
	sllNode<T> * pElem = obj.m_head;
	while (pElem) 
	{ 
		os<<(pElem->val)<<endl;
		pElem = pElem->next;
	}
	return os<<"---------------------------------------------------------------------"<<endl;

}

template <typename T>
class SLL
{
	public:
	SLL();
	~SLL();
	bool isEmpty() const;
	const T& getFront() const;
	void addFront(const T & elem);
	void removeFront();
	void print() const;
	friend ostream & operator << (ostream & os, const SLL<T> & obj);

	private:
	sllNode<T> * m_head ;

};


template <typename T>
SLL<T>::SLL():
	m_head(NULL)
{
}

template <typename T>
SLL<T>::~SLL()
{

	while (! isEmpty() ){ removeFront(); }
}

template <typename T>
bool SLL<T>::isEmpty() const{ return (m_head ? false: true) ; }

template <typename T>
const T& SLL<T>::getFront() const 
{
	if (!isEmpty()) { return m_head->val;} 
}

template <typename T>
void SLL<T>::addFront( const T& elem)
{
	sllNode<T> * pCur = new sllNode<T>();
	pCur->val = elem;
	pCur->next = m_head;
	m_head = pCur ;
	return;
}

template <typename T>
void SLL<T>::removeFront()
{
	if (! isEmpty()) 
	{
	
		sllNode<T> * pTemp = m_head ;
		m_head = pTemp->next;
		delete pTemp  ;
		pTemp = NULL ;
	}
}

template <typename T>
void SLL<T>::print() const
{
	//cout<<"-----------Printing Single Linked List "<<typeid(T).name()<<" Content ----------------------"<<endl;
	cout<<"-----------Printing Single Linked List Content ----------------------"<<endl;
	sllNode<T> * pElem = m_head;
	while (pElem) 
	{ 
		cout<<(pElem->val)<<endl;
		pElem = pElem->next;
	}
	cout<<"---------------------------------------------------------------------"<<endl;
}



int main(int argc, const char *argv[])
{
	cout<<"Test String SLL"<<endl;
	SLL<string> strList;
	strList.addFront("Yosi");
	strList.addFront("is");
	strList.addFront("name");
	strList.addFront("My");
	strList.print();
	//cout<<strList;
	return 0;
}
