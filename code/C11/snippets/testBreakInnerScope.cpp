#include <iostream>

using namespace std;

int main()
{
        int i=0;
        for (; i<10; ++i)
        {

                cout<<"i="<<i<<endl;
                if (i==3)
                {
                        if(true)
                        {
                                cout<<"will inner scope break exit while loop?"<<endl;
                                break;
                        }

                }

        }

        if (i == 3) cout<<"Apparently, yes"<<endl;
}
