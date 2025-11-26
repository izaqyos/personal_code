#include <iostream>
#include <vector>
#include <string>
#include <utility>

using namespace std;

//compile on mac using $clang++ --std=c++11 uniquePaths.cpp -o uniquePaths

class Solution {
private:
    bool bDebug = false;
    vector<vector<int> > * board = nullptr;

    void init(int m, int n){
        if (bDebug) cout<<"init(), dimensions ("<<n<<", "<<m<<")"<<endl;
        board = new vector< vector<int> > (n , vector<int>(m,0));
    }

    void cleanup(){
        if (bDebug) cout<<"delete()"<<endl;
        delete board;
    }

    void printBoard(){
        if (bDebug) cout<<"printBoard()"<<endl;
        cout<<endl;
        for (auto line : *board){
            for (auto elem : line){
                cout<<elem<<", ";
            }
            cout<<endl;
        }
    }

public:
    int uniquePaths(int m, int n) {
        if (bDebug) cout<<"uniquePath(), dimensions ("<<n<<", "<<m<<")"<<endl;
        int res = 0;
        if ( (m==0) || (n==0)) return res;
        init(m,n);
        if (bDebug){
            printBoard();
        }

        
        for (int j = m-1; j>=0 ; j--){
            for (int i=n-1; i>=0 ; i--){
                if (bDebug) cout<<"uniquePath(), at cell ("<<i<<", "<<j<<")"<<endl;
                if ( (i==n-1) && (j==m-1)){
                    (*board)[i][j] = 1;
                }
                if (j<m-1){
                    (*board)[i][j] += (*board)[i][j+1];
                }
                if (i<n-1){
                    (*board)[i][j] += (*board)[i+1][j];
                }
            }
        }
        res = (*board)[0][0];
        cleanup();
        return res;        
    }
};

