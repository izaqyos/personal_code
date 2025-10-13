
#include "LinkedList.h"
#include <iostream>


template <typename T> 	std::ostream & operator << ( std::ostream & out, const LinkedListNode<T>  & me)
{
	out<<me.m_tValue ;
	return out;
}

template <typename T> LinkedListNode<T>::LinkedListNode()
{
	m_pNext = NULL;
}

template <typename T> LinkedList<T>::~LinkedList()
{
std::cout<<"LinkedList DTOR\n";

LinkedListNode<T> * pCur = m_pHead;
LinkedListNode<T> * pPrev = NULL;

while (pCur != NULL)
{
	pPrev = pCur;
	pCur = pCur->m_pNext;
	delete pPrev;
	pPrev = NULL;
}
}

template <typename T> void LinkedList<T>::addElem(T val)
{
std::cout<<"LinkedList::addElem() "<<val<<"\n";
LinkedListNode<T> * p_New = new LinkedListNode<T>();
p_New->m_tValue = val;
p_New->m_pNext = m_pHead;
m_pHead = p_New;

}

template <typename T> void LinkedList<T>::remElem(T val)
{
std::cout<<"LinkedList::remElem() "<<val<<"\n";

LinkedListNode<T> * pCur = m_pHead;
LinkedListNode<T> * pPrev = NULL;

if (m_pHead == NULL)
{
	std::cout <<"LinkedList::remElem() - empty list. nothing to do\n";
	return;
}

if (m_pHead->m_tValue == val)
{
	std::cout<<"LinkedList::remElem() - found node to delete\n";
	pCur = m_pHead->m_pNext;
	delete m_pHead;
	m_pHead = pCur;


}

pPrev = pCur; // head
pCur = pCur->m_pNext;
while (pCur != NULL)
{
	if (pCur->m_tValue == val)
	{
		std::cout<<"LinkedList::remElem() - found node to delete\n";
		pPrev->m_pNext = pCur->m_pNext;
		delete pCur;
		return;
	}
	pPrev = pCur;
	pCur = pCur->m_pNext;
}
}

template <typename T> void LinkedList<T>::printMe() const
{
std::cout<<"LinkedList::printMe() - linked list:\n";

for (LinkedListNode<T> * pItr = m_pHead ; pItr != NULL; pItr = pItr->m_pNext )
{
	LinkedListNode<T> tmp = *pItr;
	std::cout<<tmp<<"->";
}
std::cout <<"||\n";

}
