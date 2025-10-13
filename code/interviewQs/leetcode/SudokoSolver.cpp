/*
 * 
 
 */

#include <iostream>
#include <vector>
#include <bitset>
#include <array>
#include <cassert>

using namespace std;

class Solution {
public:

    struct cell
    {
        int val; //value
        int numP; //number of possible values
        bitset<10> pvals; //possible values. 0 bit means possible. 1 - impossible.
        cell():
        val(0),
        numP(9),
        pvals()
        {};
    };
    

    bool bD = true;
    array<array<cell,9> , 9> cells; //internal representation for solving
    vector<pair<int, int>> emptyCells; // list of empty cells
    
    
    
    void printBoard(vector<vector<char>>& board)
    {
        cout<<"[";
        for (int i=0;i<board.size(); ++i)
        {
            cout<<"\"";
            for(int j=0;j<board[i].size();++j)
            {
                cout<<board[i][j];
            }
            cout<<"\"";
            if (i<8) cout<<",";
        }
        cout<<"]"<<endl;
    }
    
    bool updateImpossibleVal(int i,int j,int v) //update v is not possible
    {
        cell c = cells[i][j];
        
        if (c.val == v) //oopsi 
            return false;
            
        if (c.pvals[v]) // v bit set to 1, indicating v not possible. good
            return true;
            
        c.pvals.set(v);
        c.numP--;
        if (c.numP > 1) return true; //more than one possibility. 
        
        //excatly one possibility left, why not set it and recurse...
        for (int p = 1; p<10;++p)
        {
            if (!c.pvals[p]) // found p, the only possible value. propogate it...
                propogateValue(i,j,p);
        }
        
        //we should not reach here 
        assert(0); 
    }
    
    bool propogateValue(int i,int j, int v )
    {
        if (bD) cout<<"propogateValue, "<<v<<", pos: ["<<i<<"]["<<j<<"]"<<endl;
        cell & c = cells[i][j];
        if (c.val == v) 
            {
                if (bD) cout<<"propogateValue, value was already set correctly"<<endl;
                return true; //This cell was already set correctly
            }
        if (c.pvals[v]) 
            {
                if (bD) cout<<"propogateValue, value excluded from possible values"<<endl;
                return false;//already has v excluded from possible values
            }
        
        //set cell possible values, reflecting current value v
        c.val = v;
        c.pvals = bitset<10>(0x3FE);// 0000001111111110 - 1-9 not possible
        c.pvals.reset(v); //allow v
        c.numP = 1; //wasn't empty so only one possible value, original value
        
        for (int l=0; l<9; ++l )
        {
            if (bD && (i!=l )) cout<<"restrict value from row "<<l<<", column "<<j<<endl;
            if ( (i!=l ) && !updateImpossibleVal(l,j,v)) //update all rows j column except the ith, if update fails means conflict
                return false;
                
            if (bD && (j!=l )) cout<<"restrict value from row "<<i<<", column "<<l<<endl;
            if ( (j!=l ) && !updateImpossibleVal(i,l,v)) //update all columns on ith row except the jth, if update fails means conflict
                return false;
                
                
            int ix = (i/3)*3 + l/3; // (i/3)*3 -> set begin raw of sub-box, e.g i=4, set begin raw to 3. +l/3 , every three values advance row
            int jx = (j/3)*3 + l%3; // (j/3)*3 -> set begin column of sub-box, e.g j=7, set begin column to 6. +l%3 advance colum three times per raw
            if (bD && (jx!=j ) && (ix!=i) ) cout<<"restrict value from sub-box "<<ix<<","<<jx<<endl;
            if ( (jx!=j ) && (ix!=i) && !updateImpossibleVal(ix,jx,v)) //update subbox, if fails means conflict
                return false;
        }
        
        if (bD) cout<<"propogateValue, value "<<cells[i][j].val<<" updated and restricted successfuly"<<endl;
        return true;
    }
    
    //put all empty cells in list, sort in ascending order of possible valus
    //backtrack over this list
    bool checkAndSolveEmpty()
    {
        emptyCells.clear();
        for (int i=0; i<9;++i)
        {
            for (int j=0; j<9;++j)
            {
                if ( cells[i][j].val == 0) emptyCells.push_back(make_pair(i,j));
            }
        }
        
        sort(emptyCells.begin(), emptyCells.end() ,
        [this] (const pair<int, int> & a , const pair<int, int> & b )  //lambda < operator
        {
          return (cells[a.first][a.second].numP < cells[b.first][b.second].numP);   
        }
        ); // sort empty cells by increasing order of possible values
        
        return solveRec(0); //solve by recursively trying the values of empty cells and backtracking on conflict
    }
    
    bool solveRec(int i)
    {
        if (i>= emptyCells.size()) return true; //stop condition 
        int r = emptyCells[i].first;
        int c = emptyCells[i].second;
        if (cells[r][c].val != 0 ) return solveRec(i+1); //a single value was set so rewind stack to caller w/ true
        
        array<array<cell,9> , 9> cells_copy(cells);
        //select possible values and recurse on them
        for (int j=1; j<10; ++j )
        {
            if (!cells[r][c].pvals[j]) // j is possible value
            {
                if (propogateValue(r,c,j)) //try to solve w/ j
                {
                    //if we reached here we've solved all empty cells including i, move to next
                    return solveRec(i+1);
                }
                
                //if we got here setting j to cell[r][c] is dead end, restore cells
                cells=cells_copy;
            
            }
            
            
        }//for
        
        //if we got here, solveRec can't find possible value for ith empty cell
        return false;
    }
    
    void solveSudoku(vector<vector<char>>& board) {
        //1st solution idea - too slow
        // use simple backtrack recursion.
        // 2nd - way more complex backtrack
        // do initial step of
        // constraint calculation. For each empty keep bitset of 
        // possible values and only try those.
        // if lucky, we have solution, otherwise backtrack to find solution
        
        int m = board.size();
        if (m != 9 ) return ;
        for (auto r : board)
        {
            if ( r.size() != 9) return ;
        }
        
        
        cells = array< array<cell, 9>, 9>();
        
        if (bD) cout<<"Solving board..."<<endl;
        if (bD) printBoard(board);
        
        
        char c;
        //calculate and propogate constraints
        for (int i=0;i<board.size(); ++i)
        {
            for(int j=0;j<board[i].size();++j)
            {
                c = board[i][j];
                if (bD) cout<<"handle cell["<<i<<"]["<<j<<"]="<<c<<endl;
                if ( (board[i][j] != '.') &&    !propogateValue(i,j, c  - '0' ) )
                    return;// propogateValue returns false if it found a contradiction.
            }
        }
        
        //if no empty cells we have a solution, otherwise backtrack to find one
        if (!checkAndSolveEmpty() ) return; //checkAndSolveEmpty works on internal cells representation
        //it searches for empty sells and adds them to list, then uses recursion to solve their values
        // if it returns false then no solution is possiblw
        
        
        if (bD) cout<<"Solved board..."<<endl;
        
        
        for (int i =0; i<9;++i)
        {
            for (int j=0; j<9; ++j)
            {
                //if (board[i][j] == '.') board[i][j] = cells[i][j].val+'0';
                if (cells[i][j].val) board[i][j] = cells[i][j].val+'0';
            }
        }
        printBoard(board);
    }
};

int main()
{
	vector<vector<char>>& board ={{'.','.','9','7','4','8','.','.','.'},{'7','.','.','.','.','.','.','.','.'},{'.','2','.','1','.','9','.','.','.'},{'.','.','7','.','.','.','2','4','.'},{'.','6','4','.','1','.','5','9','.'},{'.','9','8','.','.','.','3','.','.'},{'.','.','.','8','.','3','.','2','.'},{'.','.','.','.','.','.','.','.','6'},{'.','.','.','2','7','5','9','.','.'}} ;
	Solution sol;
	sol.solveSudoku(board);
}
