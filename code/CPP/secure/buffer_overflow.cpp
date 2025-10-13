   /* 
*
*       Filename:  buffer_overflow.cpp
*
*    Description:  Buffer overflow exploit
*
*        Version:  1.0
*        Created:  10/10/2012  6:04:33 PM
*       Revision:  none
*       Compiler:  gcc
*
*         Author:  YOSI IZAQ
*   Organization:  
*
* =====================================================================================
*/

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

bool IsPasswordOkay(void) {
  char Password[12];
 
  gets(Password);
  if (!strcmp(Password, "goodpass"))
    return(true);
  else
    return(false);
}
 
int main(void) {
  bool PwStatus;
 
  puts("Enter password:");
  PwStatus = IsPasswordOkay();
  if (PwStatus == false) {
    puts("Access denied");
    exit(-1);
  }
  else
    puts("Access granted");
}
