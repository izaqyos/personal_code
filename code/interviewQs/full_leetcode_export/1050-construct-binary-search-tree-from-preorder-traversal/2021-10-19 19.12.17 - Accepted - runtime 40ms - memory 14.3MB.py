class Solution:
    def utilRec(self, preorder: List[int], highLim:int):
        if not preorder or preorder[-1] > highLim:
            return None
        currentNode = TreeNode(preorder.pop())
        currentNode.left = self.utilRec(preorder, currentNode.val) #left tree hig lim is root val 
        currentNode.right = self.utilRec(preorder, highLim) #right tree hig lim starts as infinity
        return currentNode

    def bstFromPreorder(self, preorder: List[int]) -> Optional[TreeNode]:
        return self.utilRec(preorder[::-1], float('inf'))


