class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        prev_indices = []
        ret = [ 0 for _ in temperatures]
        for i,t in enumerate(temperatures):
            while prev_indices and (t > temperatures[prev_indices[-1]]):
                ret[prev_indices[-1]] = i-prev_indices[-1]
                prev_indices.pop()
            prev_indices.append(i)
        return ret