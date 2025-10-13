/*
 * =====================================================================================
 *
 *       Filename:  simpleTemplate.cpp
 *
 *    Description:  Simple template practice
 *
 *        Version:  1.0
 *        Created:  02/20/2017 15:51:06
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  YOSI IZAQ
 *   Organization:  
 *
 * =====================================================================================
 */


#include <string>

using namespace std;

template<typename T>
class myTclass
{
	public:
		myTclass(const T& t):
			m_t(t)
	{};

		void printMe() const;
	private:
		T m_t;

};

//template specialization. e.g make specific type have custom behavior
template<>
class myTclass<string>
{
	public:
		myTclass(const string & str):
			m_t(str)
	{};
		void printMe() const;
		void printReverse() const;

	private:
		string m_t;
};



