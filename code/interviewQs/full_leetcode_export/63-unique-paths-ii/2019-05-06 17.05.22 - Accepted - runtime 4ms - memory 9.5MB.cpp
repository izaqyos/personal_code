class Solution {
    
    bool bDebug = false;
    
public:
        void printGrid(vector<vector<int>> &grid)
    {
        for (auto line : grid)
        {
            for (auto elem : line)
            {
                cout << elem << ", ";
            }
            cout << endl;
        }
    }
    
           int uniquePathsWithObstacles(vector<vector<int>> &obstacleGrid)
    {
        if (bDebug)
        {
            cout << "uniquePathsWithObstacles(), got obstacle grid: " << endl;
            printGrid(obstacleGrid);
        }

        size_t n = obstacleGrid.size();
        if (n == 0)
            return 0;
        size_t m = obstacleGrid[0].size();
        if (m == 0)
            return 0;

        vector<vector<long>> paths(n, vector<long>(m, 0));
        for (size_t j = m - 1; j < m; j--) //j < m since its a unsigned int and wraps around (-1 = max value -1 )
        {
            for (size_t i = n - 1; i < n; i--)
            {
                if (bDebug)
                    cout << "at cell (" << i << ", " << j << ")" << endl;
                if ((i == n - 1) && (j == m - 1)) //"start condition"
                {
                    if (obstacleGrid[i][j] == 1)
                        return 0;            //oopsi
                    paths[i][j] = 1; //since 1 represents obstacle lets keep tabs using negatives
                }
                if (obstacleGrid[i][j] != 1) //yippi, clear path
                {
                    if ((j < m - 1) && (obstacleGrid[i][j + 1] != 1)) //we can go right :)
                    {
                        paths[i][j] += paths[i][j + 1];
                    }
                    if ((i < n - 1) && (obstacleGrid[i + 1][j] != 1)) //we can go down :)
                    {
                        paths[i][j] += paths[i + 1][j];
                    }
                }
            }
        }

        return max(paths[0][0], (long) 0);
    }
};