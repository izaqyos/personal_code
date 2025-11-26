class Solution {
public:
    void rotate(vector<vector<int>>& matrix) {
        //idea, rotate by layers, first outer then goining inside on half the diagonal
        
        int n = matrix.size();
        int t1,t2;
        for (int i=0; i< n/2; ++i)
        {
            for (int j=i;j<n-i-1; ++j)
            {
                //do four way swap 
                /*
                cout<<"Swapping 4 cells: "<<endl;
                cout<<"("<<i<<","<<j<<")"<<", value: "<<matrix[i][j]<<endl;
                cout<<"("<<j<<","<<n-1-i<<")"<<", value: "<<matrix[j][n-1-i]<<endl;
                cout<<"("<<n-1-i<<","<<n-1-j<<")"<<", value: "<<matrix[n-1-i][n-1-j]<<endl;
                cout<<"("<<n-1-j<<","<<i<<")"<<", value: "<<matrix[n-1-j][i]<<endl;
                */
                t1 = matrix[j][n-1-i];
                matrix[j][n-1-i] = matrix[i][j];
                t2 = matrix[n-1-i][n-1-j];
                matrix[n-1-i][n-1-j] = t1;
                t1=t2;
                t2= matrix[n-1-j][i];
                matrix[n-1-j][i] = t1;
                t1=t2;
                matrix[i][j] = t1;
            }
        }
    }
};