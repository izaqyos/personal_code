class Solution:
    def numRescueBoats(self, people: List[int], limit: int) -> int:
        people.sort()
        s,e=0,len(people)-1
        boats = 0
        while s<=e:
            if s == e:
                boats+=1
                break
            if people[e]+people[s]<=limit:
                boats+=1
                e-=1
                s+=1
            else:
                boats+=1
                e-=1
        return boats


