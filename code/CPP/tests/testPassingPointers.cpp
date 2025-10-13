#include <iostream>

using namespace std;

void func1 (int * pint)
{
        cout<<"Got "<<*pint<<endl;
        *pint  = (*pint)*(*pint);
        cout<<"Returning "<<*pint<<endl;
}

void func2 (int * pint)
{
        cout<<"Got "<<*pint<<endl;
        *pint  = (*pint)*(*pint);
        pint = 0;
        //This compiles. but next line will  crash
        cout<<"Returning "<<*pint<<endl;
}

void func3 (int * pint)
{
        cout<<"Got "<<*pint<<endl;
        if (pint)
        {
                cout<<"delete pint"<<endl;
                delete pint;
                pint = nullptr;
        }
}

void func4 (int** ppint)
{
        int* pint =*ppint;
        cout<<"Got "<<*pint<<endl;
        if (pint)
        {
                cout<<"delete pint"<<endl;
                delete pint;
                ppint = nullptr;
        }
}

void func5 (int*& pint)
{
        cout<<"Got "<<*pint<<endl;
        if (pint)
        {
                cout<<"delete pint"<<endl;
                delete pint;
                pint = nullptr;
        }
}

int main()
{
        int val1 = 2;
        cout<<"val1="<<val1<<endl;
        cout<<"calling func1(&val1)"<<endl;
        func1(&val1);

        cout<<"avoid calling func2(&val1) as it will crash"<<endl;
        //func2(&val1);

        int * pint = new int;
        *pint=3;
        cout<<"calling func3(pint)"<<endl;
        func3(pint);
        if (pint)
        {
            cout<<"pint="<<*pint<<endl;
        }
        else
        {
                cout<<"pint is null"<<endl;
        }

        int * pint2 = new int;
        *pint2=4;
        cout<<"calling func4(pint)"<<endl;
        func4(&pint2);
        if (pint2 !=nullptr)
        {
            cout<<"pint2="<<*pint2<<endl;
        }
        else
        {
                cout<<"pint2 is null"<<endl;
        }

        int * pint3 = new int;
        *pint3=5;
        cout<<"calling func5(pint)"<<endl;
        func5(pint3);
        if (pint3 !=nullptr)
        {
            cout<<"pint3="<<*pint3<<endl;
        }
        else
        {
                cout<<"pint2 is null"<<endl;
        }
}
