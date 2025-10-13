#include <iostream>
#include <string>
#include <vector>

using namespace std;



class Solution
{
        public:

    void printBoard( vector<string> & board)
    {
        for (auto v : board)
            cout<<v<<endl;
    }

vector<vector<string> > solveNQueens(int n) {
    vector<vector<string>> result; vector<int> r (n, -1);
    solve(result, r, 0);
    return result;
}

void solve(vector<vector<string> >& result, vector<int>& r, int curRow) {
    for(int xPos = 0; xPos<r.size(); xPos++) {
        r[curRow] = xPos;
        bool isSafe = true;
        for(int i = 0; i<curRow; i++) {
            if(r[i] == xPos || abs(curRow - i) == abs(xPos - r[i])) {
                isSafe = false;
                break;
            }
        }
        
        if(isSafe && curRow == r.size() - 1) {
            vector<string> v (r.size(), string(r.size(), '.'));
            for(int i = 0; i<r.size(); i++) 
                v[i][r[i]] = 'Q';
            result.push_back(v);
        }
        else if(isSafe) {
            solve(result, r, curRow + 1);
        }
    }
}
};

int main ()
{
        //vector<int> vInp = {0,1,2,3,4,5};
        vector<int> vInp = {4};
        Solution sol;
        vector<vector<string>> vRes;

        for ( auto nu : vInp)
                vRes = sol.solveNQueens(nu);
                for (auto v : vRes)
                {
                        cout<<"Valid solution:"<<endl;
                        sol.printBoard(v);
                }
};
