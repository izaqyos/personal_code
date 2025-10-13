/*
 * =====================================================================================
 *
 *       Filename:  sizing_strings.cpp
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  10/ 2/2012 12:34:43 PM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Yosi Izaq
 *   Organization:  
 *
 * =====================================================================================
 */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <cwchar>

int main(){

wchar_t wide_str1[] = L"0123456789";
printf ("strlen incorrect size and count of 0123456789 wide string is: %d\n", strlen((const char *)wide_str1)+1);
printf ("wcslen incorrect size, yet correct count, of 0123456789 wide string is: %d\n", wcslen(wide_str1)+1);
printf ("wcslen multiply by sizeof wchar_t correct size of 0123456789 wide string is: %d\n", (wcslen(wide_str1)+1)*sizeof(wchar_t) );
wchar_t *wide_str2 = (wchar_t *)malloc((wcslen(wide_str1)+1)*sizeof(wchar_t) );
if (wide_str2 == NULL) {
  /* Handle Error */
}
/* ... */
free(wide_str2);
wide_str2 = NULL;

}

