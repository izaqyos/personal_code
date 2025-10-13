#include <iostream>
#include <string>
#include <vector>
#include <tuple>


using namespace std;

class Solution {
public:
    enum Directions :int{right, down, left, up};
    vector<vector<int>> generateMatrix(int n) {

            //vector<vector<int>>  retMatrix(3, vector<int>(3,1));
            //return dummyMatrix; 
           int iDistance = n; 
           int iCurrDist= iDistance;
           vector<vector<int>>  retMatrix(n, vector<int>(n,0));
           int i,j;
           tie(i,j) = 0,0; //nice, like python :)
           Directions direction = Directions::right;
           totalSet = 0;
           if (bDebug) cout<<"generateMatrix() for n="n<<endl;

           while (totalSet < n*n)
           {
                   iCurrDist = iDistance;
                   if (bDebug) cout<<"[i,j]=["<<i<<","<<j<<"], totalSet="<<totalSet<<endl;

           }// while (totalSet < n*n)
    }

private:
    bool bDebug = false;
};

class Tester
{
        public:
        Tester(vector<int>& vTCs):
                m_vTCs(vTCs)
        {
        }

        printMatrix(vector<vector<int>>  matrix)
        {
//                        cout<<"[";
//                for (auto row : matrix)
//                {
//                       
//                        for (auto num : row)
//                        {
//                                cout<<num<<", ";
//
//                        }
//                }
//                        cout<<"]";
//                        cout<<endl;

                for (vector<vector<int>>::const_iterator cit = matrix.begin(); cit != matrix.end(); ++cit)
                {
                        cout<<"[";
                        for (vector<int>::const_iterator cit2 = (*cit).begin(); cit2 != (*cit).end(); ++cit2)
                        {
                                cout<<(*cit2)<<", ";
                        }
                        cout<<"]";
                        cout<<endl;
                }
                        cout<<endl;

        };

        runTests()
        {
                Solution sol;
                for (auto v : m_vTCs)
                {
                    printMatrix(sol.generateMatrix(v));
                }

        };

        private:
        vector<int> m_vTCs;
};

int main()
{
vector<int> testCases={0,1,2,3,4,5};

Tester tester(testCases);
tester.runTests();
}
