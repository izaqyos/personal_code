/*
 * =====================================================================================
 *
 *       Filename:  stdSeq.h
 *
 *    Description:  practice factory DP
 *
 *        Version:  1.0
 *        Created:  08/14/16 20:48:05
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  YOSI IZAQ
 *   Organization:  
 *
 * =====================================================================================
 */

#include <list>
#include <deque>
#include <string>

using namespace std;

template <typename T>
class aSequence
{

	public:
		virtual size_t size() const = 0;
		virtual void printMe() const = 0;

		virtual ~ aSequence(){};
	private:
		string mName;


};

template <typename T>
class aList : public aSequence<T>
{

	public:
		aList ( string sName);
		virtual size_t size() const ;
		virtual void printMe() const;

		virtual ~ aList(){};
	private:
		string mName;
		list<T> mList;
};

template <typename T>
class aDeque : public aSequence<T>
{

	public:
		aDeque ( string sName);
		virtual size_t size() const ;
		virtual void printMe() const;

		virtual ~ aDeque(){};
	private:
		string mName;
		deque<T> mDeque;
};

