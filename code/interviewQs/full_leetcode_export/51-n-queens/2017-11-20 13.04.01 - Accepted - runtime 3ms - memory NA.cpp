class Solution {
        public:
                bool bD = false;

                void printBoard( vector<string> & board)
                {
                        for (auto v : board)
                                cout<<v<<endl;
                }

                void solveNQRec(vector<vector<string>> & vret, vector<int> & rowsQLoc, int cR)
                {
                        if (bD) cout<<"Processing row "<<cR<<endl;
                        int n = rowsQLoc.size();

                        for (int cIdx = 0; cIdx<n; cIdx++)
                        {
                                bool bOk = true;
                                rowsQLoc[cR] = cIdx ; //place Q in row CR in position cIdx

                                //check safe
                                for (int i=0;i<cR; ++i)
                                {
                                        if ( (rowsQLoc[i] == cIdx) || (abs(cR-i) == abs(cIdx-rowsQLoc[i])) )
                                        {
                                                bOk =false;      
                                                break;
                                        }
                                }


                                if (bOk  && (cR==n-1))
                                {
                                if (bD) cout<<"Set Q location to ("<<cR<<", "<<cIdx<<")"<<endl;
                                                vector<string>  board(n,string(n,'.'));
                                                for (int i=0;i<n;++i)
                                                {
                                                        board[i][rowsQLoc[i]] = 'Q';
                                                }

                                                vret.push_back(board);
                                        }
                                                else if (bOk)
                                                {
                                                        solveNQRec(vret, rowsQLoc, cR+1);
                                                }

                                }


                        }

                        vector<vector<string>> solveNQueens(int n) {
                                vector<int> rowsQLoc(n, -1); // rowsQLoc[i] , location of Q in row i
                                vector<vector<string>> vret; 
                                solveNQRec(vret, rowsQLoc,0); // start at row 0 
                                return vret;

                        }
                };
