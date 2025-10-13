/*
 * =====================================================================================
 *
 *       Filename:  MemAlloc.c
 *
 *    Description:  Excersise in memory allocating functions
 *
 *        Version:  1.0
 *        Created:  04/13/2014 19:35:28
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
#include <string>
#include <vector>

using namespace std;

int f_alloc(char *** pppCharArr, unsigned int * piLen)
{

	const unsigned int ic_cells = 3;
	char str1[5] = "abcd"; 
	char str2[4] = "xxx"; 
	char str3[3] = "yy"; 
	printf("%s - Starting memory allocation function \n", __func__);

	printf("%s - calloc...\n", __func__);
	*pppCharArr = (char **) calloc(ic_cells, sizeof(char *) );
	//piLen =  calloc(1, sizeof(unsigned int ) ) ;
	*piLen = 0;
	char ** ppTmpCharArr = *pppCharArr;

	printf("%s - malloc...\n", __func__);
        ppTmpCharArr[*piLen] = (char *) malloc(strlen(str1) +1);
	printf("%s - memcpy...\n", __func__);
	memcpy(ppTmpCharArr[*piLen], str1, strlen(str1) +1); 
	printf("%s - increment...\n", __func__);
	printf("%s - Copied string is %s\n", __func__, ppTmpCharArr[*piLen] );
	(*piLen)++;

	printf("%s - 2nd malloc...\n", __func__);
        ppTmpCharArr[*piLen] = (char *) malloc(strlen(str2) +1);
	printf("%s - 2nd memcpy...\n", __func__);
	memcpy(ppTmpCharArr[*piLen], str2, strlen(str2) +1); 
	printf("%s - 2nd increment...\n", __func__);
	printf("%s - Copied string is %s\n", __func__, ppTmpCharArr[*piLen] );
	(*piLen)++;

        ppTmpCharArr[*piLen] = (char *) malloc(strlen(str3) +1);
	memcpy(ppTmpCharArr[*piLen], str3, strlen(str3) +1); 
	printf("%s - Copied string is %s. Total length is %u\n", __func__, ppTmpCharArr[*piLen], *piLen );

	printf("%s - Ptr to char** array is %p, passed %p, deref %p\n", __func__, ppTmpCharArr ,  pppCharArr ,  *pppCharArr);
	return 0;
}

int f_memUser(vector<string> & out_v)
{

	printf("%s - Starting memory allocation using function \n", __func__);
char ** ppCharArr;
unsigned int  iLen = 0;
out_v.clear();

	f_alloc(&ppCharArr, &iLen);

	printf("%s - Ptr to char** array is %p\n", __func__, ppCharArr );
	printf("%s - Returned %u length of string list\n", __func__, iLen);
	for (unsigned int i = 0; i < iLen; i++) {
		printf("Str %u is %s. Adding to out vec and freeing it...\n",i+1, ppCharArr[i]);
		out_v.push_back(ppCharArr[i]);
		free (ppCharArr[i]); 
	}


	printf("%s - Free char** array\n", __func__);
        free (ppCharArr); 

	return 0;
}

int main(int argc, const char *argv[])
{
	printf("Starting memory allocation in C demo...\n");

	vector<string> v1,v2;
	f_memUser(v1);
	f_memUser(v2);
	for (vector<string>::const_iterator i = v1.begin(); i != v1.end(); ++i) {
		printf("v1 string elem %s\n", (*i).c_str() );
	}
	for (vector<string>::const_iterator i = v2.begin(); i != v2.end(); ++i) {
		printf("v2 string elem %s\n", (*i).c_str() );
	}

	return 0;
}
