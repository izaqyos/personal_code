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