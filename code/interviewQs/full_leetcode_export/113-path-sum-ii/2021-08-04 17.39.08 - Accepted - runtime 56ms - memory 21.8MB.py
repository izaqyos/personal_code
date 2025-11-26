# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def checkSum(self, node, path, targetSum):
        sum = 0
        ret = [] 
        tpath=path[:]
        tpath.append(node)
        
        for n in tpath:    
            sum+=n.val
            ret.append(n.val)
        if sum == targetSum:
            return ret
        else:
            return []
            
        
    def ppath(self, path):
        print('->', end='')
        for n in path:
            print(str(n.val)+'->', end='')
        print('')
            
    def pathSum(self, root: TreeNode, targetSum: int) -> List[List[int]]:
        stack = [(root, [])] #(node, path2nodeList)
        ret = []
        while stack:
            c, path = stack.pop()
            
            if not c:
                continue
            if (not c.left) and (not c.right): 
                sumPath = self.checkSum(c,path, targetSum)
                if sumPath:
                    ret.append(sumPath)
                
            
            lpath = path[:]
            
            lpath.append(c)
            
            rpath = path[:]
            rpath.append(c)
            stack.append((c.right, rpath))
            stack.append((c.left, lpath))
            
        return ret
            
            
        