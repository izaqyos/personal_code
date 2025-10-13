/*
 * =====================================================================================
 *
 *       Filename:  simpleTemplate.cpp
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  02/20/2017 15:55:47
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  YOUR NAME (), 
 *   Organization:  
 *
 * =====================================================================================
 */
#include "simpleTemplate.h"

#include <iostream>
/*
 * 
 
[yizaq@YIZAQ-M-W1ZV:Mon Feb 20:~/Desktop/Work/code/C11/templates:]$ clang++ -std=c++11 simpleTemplate.cpp -o simpleTemplate
[yizaq@YIZAQ-M-W1ZV:Mon Feb 20:~/Desktop/Work/code/C11/templates:]$ ./simpleTemplate 
T: 7

 */
template<typename T> void myTclass<T>::printMe() const
{

	cout<<"T: "<<m_t<<endl;
}

//template<> 
void myTclass<string>::printMe() const
{

	cout<<"Template Specialization print string: "<<m_t<<endl;
}

//template<> 
void myTclass<string>::printReverse() const
{

	cout<<"Reverse string: "<<endl;

	string str(m_t);
	for (string::reverse_iterator rit = str.rbegin(); rit!= str.rend(); ++rit)
		cout<<*rit;

	//for (string::reverse_iterator rit = m_t.rbegin(); rit!= m_t.rend(); ++rit)
	//	cout<<*rit;

	cout<<endl;

}

template<typename K> int doublePrint(const K& k)
{
	cout<<"Double K: "<<k<<k<<endl;
	return 0;
}

int main(int argv, char **argc )
{
	myTclass<int> intCls(7);
	intCls.printMe();
	myTclass<string> strCls("I am a rock");
	strCls.printMe();
	strCls.printReverse();

	doublePrint<string>("hello ");
	return 0;
}
