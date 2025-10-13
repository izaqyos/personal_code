#include <iostream>
#include <string>
#include <vector>
#include <stdio.h>

using namespace std;

class Solution
{
public:
    bool bD = false;

    void printBoard(vector<string> &board)
    {
        for (auto v : board)
            cout << v << endl;
    }

    void solveNQRec(vector<vector<string>> &vret, vector<int> &rowsQLoc, int cR)
    {
        if (bD)
            cout << "solveNQRec(). Processing row " << cR << endl;

        int n = rowsQLoc.size();

        for (int cIdx = 0; cIdx < n; cIdx++)
        {
            bool bOk = true;
            rowsQLoc[cR] = cIdx; //place Q in row CR in position cIdx

            //check safe
            for (int i = 0; i < cR; ++i)
            {
                if ((rowsQLoc[i] == cIdx) || (abs(cR - i) == abs(cIdx - rowsQLoc[i])))
                {
                    bOk = false;
                    break;
                }
            }

            if (bOk && (cR == n - 1))
            {
                if (bD)
                    cout << "Set Q location to (" << cR << ", " << cIdx << ")" << endl;
                vector<string> board(n, string(n, '.'));
                for (int i = 0; i < n; ++i)
                {
                    board[i][rowsQLoc[i]] = 'Q';
                }

                if (bD)
                {
                    cout << "solveNQRec(). solution board " << endl;
                    printBoard(board);
                }
                vret.push_back(board);
            }
            else if (bOk)
            {
                solveNQRec(vret, rowsQLoc, cR + 1);
            }
        }
    }

    vector<vector<string>> solveNQueens(int n)
    {
        vector<int> rowsQLoc(n, -1); // rowsQLoc[i] , location of Q in row i
        vector<vector<string>> vret;
        solveNQRec(vret, rowsQLoc, 0); // start at row 0
        return vret;
    }

    int totalNQueens(int n)
    {
        vector<vector<string>> ret = solveNQueens(n);
        return ret.size();
    }
};

int main()
{
    vector<int> vInp = {0, 1, 2, 3, 4, 5};
    //vector<int> vInp = {4};
    Solution sol;
    vector<vector<string>> vRes;

    for (auto nu : vInp)
    {
        printf("%dX%d board %d queens problem has %d solutions\n", nu, nu, nu, sol.totalNQueens(nu));
        //vRes = sol.solveNQueens(nu);
    }
};
