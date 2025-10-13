/*
 * =====================================================================================
 *
 *       Filename:  test_substr.cpp
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  Tue Feb 18 11:06:28 IST 2014
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Yosi Izaq
 *   Organization:  
 *
 * =====================================================================================
 */
#include <stdlib.h>
#include <iostream>
#include <string>
using namespace std;

int main ()
{
  string str="We think in generalities, but we live in details.";
                             // quoting Alfred N. Whitehead

  str += " END!!!";

  cout << str << endl;


  return 0;
}
