"""
idea. brute force try every possible shift combination and count overlap between matrices
both rows and columns can shift between -n+1 (up/left) and n-1 (right/down)
more than that all possible 1 bits are lost
"""
class Solution:

    def isValidPosition(self, img1: List[List[int]], i: int, j: int):
        n = len(img1)
        return (i>=0 and i < n)  and (j>=0 and j < n)

    def countOverlap(self, img1: List[List[int]], img2: List[List[int]], rowOffset: int, colOffset: int) -> int:
        total = 0
        n = len(img1)
        for i in range(n):
            for j in range(n):
                if self.isValidPosition(img2, i+rowOffset, j+colOffset):
                    if img1[i][j] and img2[i+rowOffset][j+colOffset]: 
                        total+=1
        #print(f"total for rowOffset {rowOffset}, colOffset {colOffset} is {total}")
        return total


    def largestOverlap(self, img1: List[List[int]], img2: List[List[int]]) -> int:
        n = len(img1)
        lowestOffset = -n+1
        highestOffset = n-1
        rowOffset = lowestOffset
        maxTotal = float('-inf')
        while rowOffset<=highestOffset:
            colOffset = lowestOffset
            while colOffset<=highestOffset:
                total = self.countOverlap(img1, img2, rowOffset, colOffset)
                maxTotal = max(maxTotal, total)
                colOffset +=1
            rowOffset+=1
        return maxTotal