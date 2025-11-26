"""
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
        if x1 == x2 then if both are 0 (start) higher is 1st (Y1 > Y2 return 1)
        if x1 == x2 then if both are 1 (end) lower is 1st (Y1 < Y2 return 1)
        if x1 == x2 then if one is 0 and second is 1 (end) the start is higher 
        """
        if p1[0] > p2[0]:
            return 1
        elif p1[0] == p2[0]: 
            if p1[2] == p2[2]:
                if p1[2] == 0: #start points
                    if p1[1] > p2[1]:
                        return 1
                    elif p1[1] == p2[1]: 
                        return 0
                    else:
                        return -1 
                else: #end points
                    if p1[1] < p2[1]:
                        return 1
                    elif p1[1] == p2[1]: 
                        return 0
                    else:
                        return -1 
            else: #start+end
                if p1[2] == 0:
                    return 1
                else:
                    return -1 
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
        print("sorted points", points)

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
                print("point can be 0 (start) or 1 (end) only")
                break 

            if height != -1*hq[0]:
                height = -1*hq[0]
                ret.append([pt[0], height ])
        return ret