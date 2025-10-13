"""
85. Maximal Rectangle

Share
Given a rows x cols binary matrix filled with 0's and 1's, find the largest rectangle containing only 1's and return its area.

Example 1:


Input: matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]
Output: 6
Explanation: The maximal rectangle is shown in the above picture.
Example 2:

Input: matrix = []
Output: 0
Example 3:

Input: matrix = [["0"]]
Output: 0
Example 4:

Input: matrix = [["1"]]
Output: 1
Example 5:

Input: matrix = [["0","0"]]
Output: 0
 

Constraints:

rows == matrix.length
cols == matrix.length
0 <= row, cols <= 200
matrix[i][j] is '0' or '1'.
"""

class Solution:
    """
    idea. I already solved maximal rectangle in histogram problem largetRectangleInHistogram.py
    The solution is using stack for keeping track of start positions. 
    This problem can be converted into an instance of maximal rectangle in histogram. how?
    use DP approach. use an array, dp, of size len(matrix[0]). This will serve as the intermidate histogram.
    initialize it to 1st row. dp = matrix[0][:] calc max rect. update max var.
    Then for each line, if matrix[i][j] == 0, dp[j] = 0 (reason 0 can't be part of rect) 
    if value is 1, dp[j]+=1 (reason, ith row contribute 1 more cell to current line), 
    calc area, update max. at the end return max
    """
    def maximalRectangle(self, matrix):
        if (not matrix) or (not matrix[0]):
            return 0
        maximum = 0
        m,n= len(matrix), len(matrix[0])
        dp = [ int(_) for _ in  matrix[0]]
        maximum = self.largestRectangleInHistogramArea(dp)
        for i in range(1,m):
            for j in range(n):
                if int(matrix[i][j]) == 0:
                    dp[j] = 0
                elif int(matrix[i][j]) == 1: 
                    dp[j] += 1
                else:
                    print("illegal value detected")
                    return 0
            maximum = max(maximum, self.largestRectangleInHistogramArea(dp))
        return maximum


    def largestRectangleInHistogramArea(self, heights):
        """
        so for rectangle area we do width*height. 
        width is endpos-(prev-startpos+1)
        height we keep track of start positions (in a stack)
        each height > height at stack top, add it's index to stack
        each height <= height at stack top, start poping from stack so long as current height is smaller than top. if it's empty. 
        area = heights[top]*i (empty stack means that this is the lowest height so we have a low rectangle since the begining to i)
        if stack is not empty then area = heights[top]*(i - prev-top -1)  
        """
        heights.append(0) #adding 0 will ensure we enter into inner while to flush stack at the end of heights
        startpos_stack, max_area = [], 0
        for i in range(len(heights)):
            while startpos_stack and heights[startpos_stack[-1]] >= heights[i]:
                height = heights[startpos_stack.pop()]
                width = 0
                if not startpos_stack:
                    width = i
                else:
                    width = i - (startpos_stack[-1] + 1)
                max_area = max(max_area, height*width)
            startpos_stack.append(i)
        return max_area

def test():
    inputs = [
            [],
            [[]],
            [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]],
            [["1","1","1","0","0","0"],["1","1","1","0","1", "0"],["0","0","0","0","0", "0"],["0","1","1","1","1","1"],["0","1","1","1","1","1"], ["0","1","1","1","1","0"]]
            ]
    expected = [0, 0, 6, 12]
    sol = Solution()
    for inp,exp in zip(inputs, expected):
        ans = sol.maximalRectangle(inp)
        print('maximum area rectangle of  {} is {}'.format(inp, ans))
        assert(ans == exp)

    
if __name__ == "__main__":
    test()
