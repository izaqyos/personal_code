#include <vector>
#include <iostream>

using namespace std;

int main()
{

        vector<int> vInt;
        //calling on empty vector has undefined behaviour. next line will crash
        //int a = vInt.front();
        //cout<<"a="<<a<<endl;
        //

        //better use at
        
        int b = 0;
        
        try
        {
                vInt.at( vInt.size()-1);
        }
        catch (exception e)
        {
                cout<<"caught exception "<<e.what();
        }

        cout<<"b="<<b<<endl;
}
