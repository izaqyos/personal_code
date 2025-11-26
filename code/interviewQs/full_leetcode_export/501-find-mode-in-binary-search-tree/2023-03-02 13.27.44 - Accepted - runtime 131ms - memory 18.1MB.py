# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

from collections import defaultdict
class Solution:

    def util(self, root: Optional[TreeNode], freqs: dict[int, int] ) -> List[int]:
        if root !=None:
            freqs[root.val]+=1
            self.util(root.left, freqs)
            self.util(root.right, freqs)

    """
    O(n) space Solution since I use a dictionary which in worse case is size n (all nodes have unique values)
    """
    def findModeN(self, root: Optional[TreeNode]) -> List[int]:
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

    
    def handleValue(self, val: int):
        """
        Since its BST we can check for repeating values since L,R values are <= and >= parent value 
        it's not possible for L,R to be != P and for any of LL,LR, RL, RR or other descendants to be == P
        """
        print(f"handleValue:value {val}")
        print(f"handleValue: self.curr_val = {self.curr_val}, self.curr_val_count = {self.curr_val_count}, self.max_count = {self.max_count}, self.mode_count = {self.mode_count}, self.modes={self.modes}")
        
        if val != self.curr_val:
            self.curr_val = val
            self.curr_val_count = 0

        self.curr_val_count+=1
        if self.curr_val_count > self.max_count: #found new max, so modes are set to 1
            self.max_count = self.curr_val_count 
            self.mode_count = 1
        elif  self.curr_val_count == self.max_count: #found new val with same frequency as other maximum found
            self.mode_count+=1
            if (len(self.modes) > 0): # will only be true in second pass
                self.modes[self.mode_count-1] = self.curr_val


    def inOrderTraversal(self, root: Optional[TreeNode]):
        if root != None:
            self.inOrderTraversal(root.left)
            self.handleValue(root.val)
            self.inOrderTraversal(root.right)

    """
    O(1) Solution. credit to StefanPochmann who came up with the idea. 
    actually simple idea. 2 pass. 
    first pass, what is mode number (how many values of highest frequency)
    second pass, collect above values to return array
    """
    def findMode(self, root: Optional[TreeNode]) -> List[int]:
        self.curr_val = None
        self.curr_val_count = 0
        self.max_count = 0
        self.mode_count = 0
        self.modes=[]

        print(f" self.curr_val = {self.curr_val}, self.curr_val_count = {self.curr_val_count}, self.max_count = {self.max_count}, self.mode_count = {self.mode_count}, self.modes={self.modes}")
        self.inOrderTraversal(root) # first traversal, get mod count
        print(f" self.curr_val = {self.curr_val}, self.curr_val_count = {self.curr_val_count}, self.max_count = {self.max_count}, self.mode_count = {self.mode_count}, self.modes={self.modes}")

        self.modes = [0 for _ in range(self.mode_count)]
        self.curr_val_count = 0
        self.mode_count = 0

        self.inOrderTraversal(root) # second traversal, fill modes array
        return self.modes
