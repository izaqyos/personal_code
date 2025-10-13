#include <iostream>
#include <string>
#include <stdio.h>

using namespace std;

void testNullPPtr(void **pptr)
{
        string localStr("localStr");

        *pptr = (&localStr);
        printf("Pre wrong null check that will exit on valid ptr!\n");
        if (*pptr != NULL) //the wrong check!
                return;


        printf("After wrong null check try to print %s\n", (&localStr)->c_str());

}
int main()
{


        string mystr("test");
        void * pStr = &mystr;

        testNullPPtr(&pStr);

}

