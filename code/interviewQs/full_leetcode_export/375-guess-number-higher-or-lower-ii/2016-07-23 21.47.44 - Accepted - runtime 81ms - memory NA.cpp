class Solution {
public:
    int getMoneyAmount(int n) {
        if (n<=1) return 0;
        if (n==2) return 1;
        
        vector< vector<int> > sums(n, vector<int>(n,INT_MAX ));// n*n, keep value of range i,j
        
        for (int i=0; i<n; i++) sums[i][i] = 0; // the diagonal, 0 b/c no need to guess - can't get it wrong
        
        // now iterate over increasing range i,j. final res sums[0][n-1] - range 1,n
        for (int len =1; len<n; ++len)
        {
            for (int i=0; i+len<n; ++i)
            {
                int j=i+len;
                //now run over all possible guesses in range k=i ... k=j for each check
                // min(i<=k<=j){k+max(sums[i][k-1],sums[k+1,j])} - represent guessing and paying k
                // Then pay for worst case, either i..k-1 or k+1..j
                for (int k=i; k<=j; ++k)
                {
                    sums[i][j] = min(sums[i][j], k+1 +max( ((k>=i+1) ? sums[i][k-1] : 0 ) , ((k<=j-1) ? sums[k+1][j] : 0 ))); 
                    //cout<<"len: "<<len<<", i: "<<i<<", j: "<<j<<", k: "<<k<<", sums["<<i<<"]["<<j<<"]: "<<sums[i][j]<<endl;
                }
                
            }
        }
        
        return sums[0][n-1];
    }
};