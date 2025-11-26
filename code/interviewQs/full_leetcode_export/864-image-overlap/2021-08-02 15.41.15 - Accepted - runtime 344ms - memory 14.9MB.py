"""
idea. brute force try every possible shift combination and count overlap between matrices
both rows and columns can shift between -n+1 (up/left) and n-1 (right/down)
more than that all possible 1 bits are lost
"""
class Solution:

    def isValidPosition(self, img1: List[List[int]], i: int, j: int):
        n = len(img1)
        return (i>=0 and i < n)  and (j>=0 and j < n)

    def largestOverlap(self, img1: List[List[int]], img2: List[List[int]]) -> int:
        """
        create a 2 lists of i,j indices where each image has 1 bit
        count all  displacments between the lists , say img1 pos 7,9 is 1. img2 pos 11, 13 is 1
        then the lists would contain (7,9) and (11,13) and we will count -4,-4 (the displacment) as 1 
        """
        l1 = [(i,j) for i,row in enumerate(img1) for j,elem in enumerate(row) if elem]
        l2 = [(i,j) for i,row in enumerate(img2) for j,elem in enumerate(row) if elem]
        import collections
        counts = collections.Counter((img1X-img2X,img1Y-img2Y) for img1X, img1Y in l1 for img2X,img2Y in l2)
        return max(counts.values() or [0])



