/*
 * =====================================================================================
 *
 *       Filename:  test_substr.cpp
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  01/14/2013  5:23:30 PM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Yosi Izaq
 *   Organization:  
 *
 * =====================================================================================
 */
#include <stdlib.h>
// string::substr
#include <iostream>
#include <string>
using namespace std;

int main ()
{
  string str="We think in generalities, but we live in details.";
                             // quoting Alfred N. Whitehead
  string str2, str3, str4;
  size_t pos;

  str2 = str.substr (12,12); // "generalities"

  pos = str.find("live");    // position of "live" in str
  str3 = str.substr (pos);   // get from "live" to the end

  cout << str2 << ' ' << str3 << endl;

  if (str.find('!') != string::npos )
  {
  str4 = str.substr(str.find('!'));
  cout<<"substr of npos: "<<str4<<endl;
  }
  else
  {
	  cout<<"substr not found";
  }

  return 0;
}
