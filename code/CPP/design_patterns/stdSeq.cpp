/*
 * =====================================================================================
 *
 *       Filename:  stdSeq.cpp
 *
 *    Description:  practice factory DP
 *
 *        Version:  1.0
 *        Created:  08/14/16 20:58:01
 *       Revision:  none
 *       Compiler:  gcc
 *         Author:  YOSI IZAQ
 *
 *   Organization:  
 *
 * =====================================================================================
 */

#include "stdSeq.h"
#include <iostream>



template <typename T> aList<T>::aList( string sName):
	mName(sName),
	mList()

{

}


template <typename T> size_t aList<T>::size() const
{
	return mList.size();
}

template <typename T> void  aList<T>::printMe() const
{
	cout<<"This is a "<<mName<<endl;
}



template <typename T> aDeque<T>::aDeque( string sName):
	mName(sName),
	mDeque()

{

}


template <typename T> size_t aDeque<T>::size() const
{
	return mDeque.size();
}

template <typename T> void  aDeque<T>::printMe() const
{
	cout<<"This is a "<<mName<<endl;
}

template class aList<int>;
template class aDeque<int>;
