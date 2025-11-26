class Solution:
    def stoneGame(self, piles: List[int]) -> bool:
        A, L = 0, 0
        T=1
        while piles:
            if piles[-1] > piles[0]:
                if T:
                    A += piles.pop()
                else:
                    L += piles.pop()
            elif piles[-1] < piles[0]:
                if T:
                    A += piles.pop(0)
                else:
                    L += piles.pop(0)
            else:
                if T:
                    A += piles.pop()
                else:
                    L += piles.pop()
            if T:
                T = 0
            else:
                T = 1
        if A > L:
            return True
        else:
            return False
                
        