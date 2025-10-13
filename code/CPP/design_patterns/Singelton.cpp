/*
 * =====================================================================================
 *
 *       Filename:  Singelton.cpp
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  08/16/16 14:45:17
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  YOUR NAME (), 
 *   Organization:  
 *
 * =====================================================================================
 */
#include <iostream>
#include "Singelton.h"

Singelton* Singelton::mp_instance = NULL;

Singelton * Singelton::instance()
{
	if (! mp_instance) 
	{
		mp_instance = new Singelton();
	}
	return mp_instance;
}

void Singelton::setName(const string & name)
{
	ms_name = name;
}

const string & Singelton::getName() const
{
	return ms_name;
}

int main(int argc, char * argv[])
{

	Singelton::instance()->setName("Yosi");
	cout<< Singelton::instance()->getName()<<endl;
}
