class Solution:
    def helper(self, piles, A, L, T, I):
        if not piles:
            if A>L:
                return True
            else:
                return False
        if T:
            A+=piles.pop(I)
            T = 0
        else:
            L+=piles.pop(I)
            T = 1
        return self.helper(piles, A, L, T, 0) or self.helper(piles, A, L, T, len(piles)-1)

    def stoneGame(self, piles: List[int]) -> bool:
        A, L = 0, 0
        T=1
        return self.helper(piles, A, L, T, 0) or self.helper(piles, A, L, T, len(piles)-1)

                
        