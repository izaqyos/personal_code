/*
 * =====================================================================================
 *
 *       Filename:  Singelton.h
 *
 *    Description:  Simple Singelton
 *
 *        Version:  1.0
 *        Created:  08/16/16 14:38:04
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

class Singelton
{

	public:
		static Singelton * instance();
		void setName(const string & name);
		const string & getName() const;
	private:
		Singelton(){}; //default CTOR - inaccessible
		Singelton(Singelton const & other){}; //copy CTOR - inaccessible
		Singelton & operator = (Singelton const& other) { return *this; } ; //= operator - inaccessible
		static Singelton * mp_instance;
		string ms_name;

};
