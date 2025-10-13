#include <iostream>

using namespace std;

int main()
{

        int * iarr = new int[10];

        delete iarr;

        cout<<"array ptr val: "<<iarr<<endl;

        delete iarr;
        cout<<"after double delete array ptr val: "<<iarr<<endl;

        if (iarr) cout<<"oops it looks like its safe to work with this pointer"<<endl;

        iarr = NULL;
        delete iarr;
        cout<<"after delete of null array ptr val:  "<<iarr<<endl;
}
