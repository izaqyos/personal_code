"""
Container With Most Water
Given n non-negative integers a1, a2, ..., an , where each represents a point at coordinate (i, ai). n vertical lines are drawn such that the two endpoints of line i is at (i, ai) and (i, 0). Find two lines, which together with x-axis forms a container, such that the container contains the most water.

Note: You may not slant the container and n is at least 2.
The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. In this case, the max area of water (blue section) the container can contain is 49.
Example:
Input: [1,8,6,2,5,4,8,3,7]
Output: 49

"""
class Solution:
    """
    brute force try all pairs of lines. o(n^2)
    how can we improve. lets consider. how can we get the max water.
    clearly our best chance is when width is maximum 
    but we need also to take highest vertical lines pairs minimum. (min(l1,l2))
    so we can do an o(n) shrinking window search
    start w/ l1 ln. move the shorter of the two until the window closes. keep track of max. 
    """
    def maxArea(self, height):
        if len(height) < 2:
            return 0
        maxwater = 0
        l,r = 0, len(height)-1
        while l<r:
            maxwater = max(maxwater, (r-l)*(min(height[l], height[r])))
            if height[l] <= height[r]: # l is shorter so move to next left line
                l+=1
            else:
                r-=1
        return maxwater


def test():
    inputs = [
        [],
        [1],
        [1,1],
        [1,8,6,2,5,4,8,3,7]
    ]
    expected = [0, 0, 1, 49]
    sol = Solution()
    for inp,exp in zip(inputs, expected):
        water = sol.maxArea(inp)
        print('max water of lines {} is {}'.format(inp, water))
        assert(water == exp)

        
if __name__ == "__main__":
    test()
