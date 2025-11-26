from collections import defaultdict
class Solution:

    def util(self, root: Optional[TreeNode], freqs: dict[int, int] ) -> List[int]:
        if root !=None:
            freqs[root.val]+=1
            self.util(root.left, freqs)
            self.util(root.right, freqs)

    def findMode(self, root: Optional[TreeNode]) -> List[int]:
        freqs = defaultdict(int)
        self.util(root, freqs)
        print(freqs)
        freqs_pairs = [(v, k) for k,v in freqs.items()]
        freqs_pairs.sort()
        print(freqs_pairs)
        ret =  [freqs_pairs[-1][1]]
        top_freq = freqs_pairs[-1][0]
        freqs_pairs.pop()
        while   freqs_pairs and freqs_pairs[-1][0] == top_freq:
            ret.append(freqs_pairs[-1][1])
            freqs_pairs.pop()

        return ret
