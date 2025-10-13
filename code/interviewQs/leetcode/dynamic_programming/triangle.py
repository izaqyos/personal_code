#!/opt/homebrew/bin/python3

from typing import List
"""
Given a triangle array, return the minimum path sum from top to bottom.

For each step, you may move to an adjacent number of the row below. More formally, if you are on index i on the current row, you may move to either index i or index i + 1 on the next row.
Example 1:

Input: triangle = [[2],[3,4],[6,5,7],[4,1,8,3]]
Output: 11
Explanation: The triangle looks like:
   2
  3 4
 6 5 7
4 1 8 3
The minimum path sum from top to bottom is 2 + 3 + 5 + 1 = 11 (underlined above).

Example 2:

Input: triangle = [[-10]]
Output: -10

Constraints:
1 <= triangle.length <= 200
triangle[0].length == 1
triangle[i].length == triangle[i - 1].length + 1
-104 <= triangle[i][j] <= 104

Follow up: Could you do this using only O(n) extra space, where n is the total number of rows in the triangle?

Idea: DP starts as last row of triangle dp = [ triangle[n-1] ] where n = len(triangle)
then double loop in reverse over lines from n-2 to 0, in each line i from 0 to length of line -1
dp[i][j] = triangle[i][j] + min(dp[i+1][j], dp[i+1][j+1])
return dp[0][0]

For challenge O(n) space I'm not sure 
"""

class Solution:
    def minimumTotalON(self, triangle: List[List[int]]) -> int:
        if not triangle:
            return -1
        m = len(triangle)
        if m == 1 :
            return triangle[0][0]

        dp = [0 for _ in range(m+1) ]
        iplus1val, temp = 0,0
        for i in range(m-1, -1, -1):
            iplus1val = dp[i+1] 
            for j in range(i, -1, -1):
                temp = dp[j]
                print(f"i={i}, j={j}, temp={temp}, dp[j]=triangle[i][j]={triangle[i][j]} + min(dp[j]={dp[j]}, iplus1val={iplus1val})")
                dp[j]=triangle[i][j] + min(dp[j], iplus1val)
                iplus1val = temp
        return dp[0]

                  """
illustrate how it works. ex triangle:
   2
  3 4
 6 5 7
4 1 8 3
Run with prints:
last triangle row is basically copied into DP. we have extra cell in DP for initializing the last row.
i=3, j=3, temp=0, dp[j]=triangle[i][j]=3 + min(dp[j]=0, iplus1val=0)
i=3, j=2, temp=0, dp[j]=triangle[i][j]=8 + min(dp[j]=0, iplus1val=0)
i=3, j=1, temp=0, dp[j]=triangle[i][j]=1 + min(dp[j]=0, iplus1val=0)
i=3, j=0, temp=0, dp[j]=triangle[i][j]=4 + min(dp[j]=0, iplus1val=0)
At this point all dp - last cell is copy of last row
next we use the next row j,j+1 plus the min of values (dp[j] and iplus1val ) to update dp[j]
i=2, j=2, temp=8, dp[j]=triangle[i][j]=7 + min(dp[j]=8, iplus1val=3)
i=2, j=1, temp=1, dp[j]=triangle[i][j]=5 + min(dp[j]=1, iplus1val=8)
i=2, j=0, temp=4, dp[j]=triangle[i][j]=6 + min(dp[j]=4, iplus1val=1)
so for 2nd from last row we now have al DP values updated
                  and so on...
i=1, j=1, temp=6, dp[j]=triangle[i][j]=4 + min(dp[j]=6, iplus1val=10)

                  """


    def minimumTotal(self, triangle: List[List[int]]) -> int:
        """
        complexity. time: O(n^2) n rows of lenghts 1..n, space complexity O(n^2) since DP is in triangle size
        """
        if not triangle:
            return -1
        m = len(triangle)
        if m == 1 :
            return triangle[0][0]

        dp = [ [ _ for _ in row] for row in triangle ]
        for i in range(m-2,-1,-1):
            for j in range(len(triangle[i])):
               dp[i][j] = triangle[i][j] + min(dp[i+1][j], dp[i+1][j+1])

        return dp[0][0]
