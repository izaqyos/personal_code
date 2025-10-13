#ifndef __LINKED_LIST____
#define __LINKED_LIST____
	
#include <ostream>


template <typename T> class LinkedListNode; //fwd decl for line below:
template <typename T> std::ostream & operator << ( std::ostream & out, const LinkedListNode<T> & me); // template specialization 
template <typename T>
class LinkedListNode
{
	public:
	LinkedListNode();
	LinkedListNode * m_pNext;
	T m_tValue;

	friend std::ostream & operator << <> ( std::ostream & out, const LinkedListNode & me);
};

template <typename T>
class LinkedList
{
	public:
	~LinkedList();
	void addElem(T val) ;
	void remElem(T val);
	void printMe() const;
	
	protected:

	private:
	LinkedListNode<T> * m_pHead;
};

#include "LinkedList.cpp" // for impl 
#endif
