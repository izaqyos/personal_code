# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    cont = True
    def findnode(self, root: 'TreeNode', p: 'TreeNode', path, cont):
        npath = path[:]
        if not root or not self.cont:
            return []
        #print('at {}, looking for {}, cont {}'.format(root.val, p.val, cont))
        if root.val == p.val:
            self.cont = False
            npath.append((root, root.val))
            return npath
        npath.append((root, root.val))
        
        pleft = self.findnode(root.left, p, npath, self.cont)
        pright = self.findnode(root.right, p, npath, self.cont)
        if pleft:
            return pleft
        if pright:
            return pright
        
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        path2p = []
        path2p = self.findnode(root, p, path2p, self.cont)
        self.cont = True
        
        path2q = []
        path2q = self.findnode(root, q, path2q, self.cont)
        pasc = {_ for _ in path2p}
        qasc = {_ for _ in path2q}
        
        #pvals = [_[1] for _ in path2p]
        #print(pvals)
        #qvals = [_[1] for _ in path2q]
        #print(qvals)
        
        intersection = pasc.intersection(qasc)
        intersection_list = [ _ for _ in intersection]
        intersection_list.sort(key= lambda x: x[1])
        return intersection_list[0][0]
        