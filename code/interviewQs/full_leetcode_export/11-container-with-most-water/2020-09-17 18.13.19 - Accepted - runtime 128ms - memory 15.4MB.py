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
        maxwater = 0
        l,r = 0, len(height)-1
        while l<r:
            maxwater = max(maxwater, (r-l)*(min(height[l], height[r])))
            if height[l] <= height[r]: # l is shorter so move to next left line
                l+=1
            else:
                r-=1
        return maxwater