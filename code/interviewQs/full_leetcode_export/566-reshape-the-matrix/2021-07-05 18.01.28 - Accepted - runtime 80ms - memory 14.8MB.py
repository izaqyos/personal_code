class Solution:
    def matrixReshape(self, mat: List[List[int]], r: int, c: int) -> List[List[int]]:
        m = len(mat)
        if m == 0:
            return mat
        n = len(mat[0])
        if n == 0:
            return mat
        if m*n != r*c:
            return mat
        
        rmat = []
        nr,nc = 0,0
        nrow=[]
        for i,row in enumerate(mat):            
            for j,col in enumerate(row):
                if nc<c:
                    nrow.append(col)
                    nc+=1
                else:
                    nc=1
                    rmat.append(nrow)
                    nrow = [col]
        if nc==c:
            rmat.append(nrow)
        return rmat
                    