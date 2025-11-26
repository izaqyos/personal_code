"""
Given n non-negative integers representing the histogram's bar height where the width of each bar is 1, find the area of largest rectangle in the histogram.
Above is a histogram where width of each bar is 1, given height = [2,1,5,6,2,3].
The largest rectangle is shown in the shaded area, which has area = 10 unit.
Example:

Input: [2,1,5,6,2,3]
Output: 10
"""

class Solution:
    def largestRectangleArea(self, heights):
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


