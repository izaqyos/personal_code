class Solution {
public:
    vector<int> spiralOrder(vector<vector<int>>& matrix) {
        
        bool bD = false;
        vector<int> vRet;
        int n = matrix.size();
        if (n == 0) return vRet;
        
        int m = matrix[0].size();
        if (m == 0) return vRet;
        
        enum class Directions {right, down, left, up};
        Directions dir = Directions::right;
        int i=0,j=0;
        int Rlim=m, Dlim=n, Llim = -1, Ulim = 0; //stop limits for right, down, left and up directions
        
        //Various stop conds can be used. boolean flag set when one of directions is exhausted.
        //or when vRet.size() == m*n
        
        bool bRun = true;
        while (bRun)
        {
            if (bD) cout<<"Cont. run? "<<(bRun?"yes":"no")<<"; i="<<i<<", j="<<j<<", Rlim="<<Rlim<<", Dlim="<<Dlim<<", Llim="<<Llim<<", Ulim="<<Ulim<<", dir= "<<(int)dir<<endl;
            switch (dir)
            {
                case Directions::right:
                     if (bD) cout<<"going right..."<<endl;
                    if (j>= Rlim) 
                    {
                        bRun =false; 
                        break;
                    }
                    
                    while (j < Rlim)
                    {
                        vRet.push_back(matrix[i][j]);
                        j++;
                         if (bD) cout<<"in while"<<endl;
                    }
                     if (bD) cout<<"after while"<<endl;
                    Rlim--;
                    i++;
                    j--;
                    dir = Directions::down;
                     if (bD) cout<<" Change dir to "<<(int)dir<<endl;
                    break;
                case Directions::down:
                    if (i>=Dlim) 
                    {
                        bRun =false; 
                        break;
                    }
                    while (i<Dlim)
                    {
                        vRet.push_back(matrix[i][j]);
                        i++;
                    }
                    Dlim--;
                    j--;
                    i--;
                    dir = Directions::left;
                    break;
                case Directions::left:
                    if (j<= Llim) 
                    {
                        bRun =false; 
                        break;
                    }
                    while (j > Llim)
                    {
                        vRet.push_back(matrix[i][j]);
                        j--;
                    }
                    Llim++;
                    i--;
                    j++;
                    dir = Directions::up;
                    break;
                case Directions::up:
                    if (i<=Ulim) 
                    {
                        bRun =false; 
                        break;
                    }
                    while (i > Ulim)
                    {
                        vRet.push_back(matrix[i][j]);
                        i--;
                    }
                    Ulim++;
                    j++;
                    i++;
                    dir = Directions::right;
                    break;
                default:
                    cout<<"Illegal direction!"<<endl;
            }
        }//while, stop cond, when one of directions is blocked
        
        return vRet;
    }
};