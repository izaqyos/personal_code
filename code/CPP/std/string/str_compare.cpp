/*
 * =====================================================================================
 *
 *       Filename:  str_compare.cpp
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  08/06/15 11:40:04
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

int main ()
{
	  std::string str1 ("green apple");
	    std::string str2 ("red apple");
	    std::string str3 ("gre");

	      if (str1.compare(str2) != 0)
		          std::cout << str1 << " is not " << str2 << '\n';

	        if (str1.compare(6,5,"apple") == 0)
			    std::cout << "still, " << str1 << " is an apple\n";

		  if (str2.compare(str2.size()-5,5,"apple") == 0)
			      std::cout << "and " << str2 << " is also an apple\n";

		    if (str1.compare(6,5,str2,4,5) == 0)
			        std::cout << "therefore, both are apples\n";

		    if (str1.compare(0,str1.size(),str1) == 0)
			        std::cout << "Prefix matches \n";
		      return 0;
}

