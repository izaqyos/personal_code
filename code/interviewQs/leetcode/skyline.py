"""
A city's skyline is the outer contour of the silhouette formed by all the buildings in that city when viewed from a distance. Now suppose you are given the locations and height of all the buildings as shown on a cityscape photo (Figure A), write a program to output the skyline formed by these buildings collectively (Figure B).

Buildings  Skyline Contour
The geometric information of each building is represented by a triplet of integers [Li, Ri, Hi], where Li and Ri are the x coordinates of the left and right edge of the ith building, respectively, and Hi is its height. It is guaranteed that 0 ≤ Li, Ri ≤ INT_MAX, 0 < Hi ≤ INT_MAX, and Ri - Li > 0. You may assume all buildings are perfect rectangles grounded on an absolutely flat surface at height 0.

For instance, the dimensions of all buildings in Figure A are recorded as: [ [2 9 10], [3 7 15], [5 12 12], [15 20 10], [19 24 8] ] .

The output is a list of "key points" (red dots in Figure B) in the format of [ [x1,y1], [x2, y2], [x3, y3], ... ] that uniquely defines a skyline. A key point is the left endpoint of a horizontal line segment. Note that the last key point, where the rightmost building ends, is merely used to mark the termination of the skyline, and always has zero height. Also, the ground in between any two adjacent buildings should be considered part of the skyline contour.

For instance, the skyline in Figure B should be represented as:[ [2 10], [3 15], [7 12], [12 0], [15 10], [20 8], [24, 0] ].

Notes:

The number of buildings in any input list is guaranteed to be in the range [0, 10000].
The input list is already sorted in ascending order by the left x position Li.
The output list must be sorted by the x position.
There must be no consecutive horizontal lines of equal height in the output skyline. For instance, [...[2 3], [4 5], [7 5], [11 5], [12 7]...] is not acceptable; the three lines of height 5 should be merged into one in the final output as such: [...[2 3], [4 5], [12 7], ...]

Attemp sweeping line algorithm.
For the output the import metric is the hieght since a higher building will overshadow a shorter one. 
So we want a vertical sweeping line going left to right.
The points (x,y,h) should be split into two (x,h,s) , (y,h,e) b/c it's important when a building starts (its height plays a role) or ends (height no longer plays a role)
so we need to sort the points by point[0] (x location).
We will also need a max heap for the current max height. and we examine point by point ascending order. any time height is changed we emit current x and h
When we encounter a single point if it is a start we add it's h to heap. if maxh changed emit x,h
When we encounter a single point if it is a end we remove it's h from heap. if maxh changed emit x,h

if there are multiple points in same x we need tie breaker rules. I gave examples and explanation in a note.
There are three.
a. one or more overlapping start points
higher is processed first to avoid adding shorter to output
b. one or more overlapping end points
lower is processed first to avoid adding lower to output
c. one or more overlapping start and end points
start is processed first, to avoid adding ends to output...
"""

class Solution:

    def splitBuildings(self, buildings):
        """
        split (Xstart, Xend, Yheight) triplets to 
        (Xstart/end, Yheight, 0/1) where 0/1 stands for start/end
        """
        points = []

        for b in buildings:
            points.append((b[0], b[2], 0))
            points.append((b[1], b[2], 1))

        return points

    def mysort(self, p1, p2):
        """
        sort by x
        if x1 == x2 then if both are 0 (start) higher is 1st (eg smaller, meaning Y1 > Y2 return -1)
        if x1 == x2 then if both are 1 (end) lower is 1st (Y1 < Y2 return -1)
        if x1 == x2 then if one is 0 and second is 1 (end) then start should be 1st so start return -1 (smaller) 
        """
        if p1[0] > p2[0]:
            return 1
        elif p1[0] == p2[0]: 
            if p1[2] == p2[2]:
                if p1[2] == 0: #start points
                    if p1[1] > p2[1]:
                        return -1
                    elif p1[1] == p2[1]: 
                        return 0
                    else:
                        return 1 
                else: #end points
                    if p1[1] < p2[1]:
                        return -1
                    elif p1[1] == p2[1]: 
                        return 0
                    else:
                        return 1 
            else: #start+end
                #print('start {}, end {}'.format(p1, p2))
                if p1[2] == 0:
                    return -1
                else:
                    return 1 
        else:
            return -1

    def getSkyline(self, buildings):
        ret = []
        if len(buildings) == 0:
            return ret

        points = self.splitBuildings(buildings)
        from functools import cmp_to_key
        mysortkey = cmp_to_key(self.mysort)
        points.sort(key= mysortkey)
        #print("sorted points", points)

        import heapq
        hq = []
        heapq.heappush(hq, 0)
        height = 0
        #now we can start. we need the heights heap and process the points. start add the heap. end remove. change height -> add to output
        for pt in points:
            #print('sweeping line encountered height {}, examine point {}. heights heap {}'.format( height, pt, hq))
            if pt[2] == 0:
                heapq.heappush(hq, -1*pt[1])
            elif pt[2] == 1:
                hq.remove(-1*pt[1])
                heapq.heapify(hq) 
            else:
                #print("point can be 0 (start) or 1 (end) only")
                break 

            if height != -1*hq[0]:
                height = -1*hq[0]
                ret.append([pt[0], height ])
        return ret



def test():
    inputs = [ 
        [],
        [[0,2,3],[2,5,3]],
     [[1,3,4],[4,7,6] ],
     [ [2,9,10], [3,7,15], [5,12,12], [15,20,10], [19,24,8] ] 
    ]
    outputs = [
        [],
        [[0,3],[5,0]],
        [[1, 4], [3, 0], [4, 6],[7, 0]] ,
        [ [2,10], [3,15], [7,12], [12,0], [15,10], [20,8], [24, 0] ]
    ]

    sol = Solution()
    for i,o in zip(inputs, outputs):
        oo = sol.getSkyline(i)
        print('Sky line for {} is\n{}'.format(i,oo))
        assert(oo == o)
        #for i in range(len(o)): 
        #    assert(oo[i] == o[i])




if __name__ == "__main__":
    test()