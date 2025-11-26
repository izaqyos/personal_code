class Solution {

    bool bDebug = false;

public:
    int minPathSum(vector<vector<int>>& grid) {
        if ( ( grid.size() == 0 ) || (grid[0].size() == 0) ) return 0;

        int n = grid.size();
        int m = grid[0].size();
        if (bDebug) cout<<"calculating min path sum for "<<m<<"X"<<n<<" grid"<<endl;

        vector<vector<int>> pathSums(n, vector<int>(m));

        pathSums[n-1][m-1] = grid[n-1][m-1];
        for (int i=n-1; i>=0; i--){
            for (int j=m-1; j>=0; j--){
                if (bDebug) cout<<"calculating min path sum for "<<i<<"X"<<j<<" grid"<<endl;
                if ( (i==n-1) && (j==m-1) ){
                    continue;
                }
                else if (j == m-1) {
                    pathSums[i][j] = grid[i][j] + pathSums[i+1][j] ;
                }
                else if (i == n-1) {
                    pathSums[i][j] = grid[i][j] + pathSums[i][j+1] ;
                }
                else{
                    pathSums[i][j] = grid[i][j] + min( pathSums[i][j+1] , pathSums[i+1][j]) ;
                }
            }
        }

        return pathSums[0][0];
    }
};
