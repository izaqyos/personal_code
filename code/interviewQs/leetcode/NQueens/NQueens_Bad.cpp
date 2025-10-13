#include <iostream>
#include <string>
#include <vector>

using namespace std;


class Solution {
public:
    bool bD = true;
    
    void printBoard( vector<string> & board)
    {
        for (auto v : board)
            cout<<v<<endl;
    }
    
    bool setQueen(vector<string> & cpBoard, int i, int j)
    {
        
        int n = cpBoard.size();
        
        if ( (cpBoard[i][j] == 'Q') || (cpBoard[i][j] == 'A') )
        {
                return false;
        }

        //found legitimate spot for queen. set all attacked slots then queen.
        for (int k=0; k<cpBoard.size(); ++k)
        {
            cpBoard[i][k] = 'A';
            cpBoard[k][j] = 'A';
        }
        
        int iD=i-1, jD=j-1;
        while ((iD >0) && (jD>0)) //diagonal up left
        {
            cpBoard[iD][jD] = 'A';
            iD--;
            jD--;
        }
        
        iD=i+1, jD=j+1;
        while ((iD < n ) && (jD< n )) //diagonal down right
        {
            cpBoard[iD][jD] = 'A';
            iD++;
            jD++;
        }
        
        iD=i-1, jD=j+1;
        while ((iD >0) && (jD<n)) //diagonal up right
        {
            cpBoard[iD][jD] = 'A';
            iD--;
            jD++;
        }
        
        iD=i+1, jD=j-1;
        while ((iD < n) && (jD > 0)) //diagonal down left
        {
            cpBoard[iD][jD] = 'A';
            iD++;
            jD--;
        }
        
        
        cpBoard[i][j] = 'Q';

        return true;
    }
    
    void normalizeBoard(vector<string> & board)
    {
        if (bD) cout<<"Normalizing board"<<endl;
        
        
        for (auto & s : board)
        {
            for (auto & c : s)
            {
                if (c == 'A') 
                {
                    if (bD) cout<<"Converting A to ."<<endl;
                    c = '.';
                }
            }
        }
        return;
    }
    
    /*
    bool solveNQueensRec(int ip, int jp, int &n, vector<string> & board, vector<vector<string>> & vret)
    {
         int s = board.size();
     
        
        if ( ( ip<0) || ( ip>=s)) return false;
        if ( ( jp<0) || ( jp>=s)) return false;
        
        
        if (bD)
        {
          cout<<"i: "<<ip<<", j: "<<jp<<", Num Queens: "<<n<<", board: "<<endl;
           // cout<<"Num Queens: "<<n<<", board: "<<endl;
            printBoard(board);
        }
        
        if (n == 0 )
        {
            if (bD) cout<<"Reached stop condition n == 0"<<endl;
                if (!board.empty())
                {
                    normalizeBoard(board);
                    //vret.push_back(board);
                    vret.insert(vret.begin(), board);
                }
                 return true;
        }
       
        
       
        //int ip=0, jp=0;
        //Try to place queen
        vector<string> cpBoard = board;
        if (setQueen(cpBoard, ip,jp)) 
        {
            n--;
        
            int i = ip;
            int j = jp;
            
            j++;
            if (j == s)
            {
                i++;
                ip=i; //we need indication in recursion loop when to reset j to 0
                j=0;
                if (i == s) return false;
            }
        //recures
            for (; i<s; ++i)
            {
                if (i>ip) j=0; //for next lines reset jp to 0 so attempt all cells in line
                for (; j<s; ++j)
                {
                    if (bD) cout<<"Recursing to ("<<i<<", "<<j<<")"<<endl;
                    //if ( (board[i][j] == 'Q') || (board[i][j] == 'A') ) continue; // occupied or threatened
                    
                    
                    return solveNQueensRec(i,j,n, cpBoard, vret);
                }
                
            }
        
        }
        else
        {
            jp++;
            if (jp == s)
            {
                ip++;
                jp=0;
                if (ip == 0) return false;
                return solveNQueensRec(ip,jp,n, cpBoard, vret);
            }
        }
        
        return false;

    }
*/

    bool solveNQueensRec(int ip, int jp, int &n, vector<string> & board, vector<vector<string>> & vret)
    {
         int s = board.size();
     
        
        if ( ( ip<0) || ( ip>=s)) return false;
        if ( ( jp<0) || ( jp>=s)) return false;
        
        
        if (bD)
        {
          cout<<"i: "<<ip<<", j: "<<jp<<", Num Queens: "<<n<<", board: "<<endl;
           // cout<<"Num Queens: "<<n<<", board: "<<endl;
            printBoard(board);
        }
        
        if (n == 0 )
        {
            if (bD) cout<<"Reached stop condition n == 0"<<endl;
                if (!board.empty())
                {
                    normalizeBoard(board);
                    //vret.push_back(board);
                    vret.insert(vret.begin(), board);
                }
                 return true;
        }
       
        
       
        //Try to place queen
        vector<string> cpBoard = board;
        if (setQueen(cpBoard, ip,jp)) 
        {
            n--;
        
        }
        //else
        //{
        //}
        
        int i = ip;
        int j = jp;
        
        j++;
        if (j == s)
        {
            i++;
            ip=i; //we need indication in recursion loop when to reset j to 0
            j=0;
            if (i == s) return false;
        }
        //recures
        solveNQueensRec(i,j,n, cpBoard, vret);
        //return false;

    }

    
    vector<vector<string>> solveNQueens(int n) {
        vector<string> board(n, string(n,'.'));
        vector<vector<string>> vret;
        
        if (n == 0) return vret;
        if (n == 1)
        {
           board[0][0]='Q';
            vret.push_back(board);
        }
        
        //initBoard(board);
       // printBoard(board);
        
        //1st idea. simple recursion
        // mark board w/ 'Q' for queen. 'A' for attacked (change to '.' before adding to vret)
        // '.' free
        // so loop over available spots. put queen, n--, mark 'A' spots (diagonal, horizontal and vertical)
        // if no place to put queen return
        // if stop condition (n==0) add board to vret and return
        
        /*
        for (int i=0; i<n; ++i)
        {
            for (int j=0; j<n; ++j)
            {
                solveNQueensRec(i,j, n, board, vret);
            }
        }
        */
        
        solveNQueensRec(0,0, n, board, vret);
      //  solveNQueensRec(n, board, vret);
        
        return vret;
        
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
}
