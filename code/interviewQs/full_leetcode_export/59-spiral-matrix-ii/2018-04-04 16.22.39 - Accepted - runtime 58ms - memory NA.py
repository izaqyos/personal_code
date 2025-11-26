def genNumsToSquare(n):
    num = 1
    while num <= n*n:
        yield num 
        num = num+1


        
class Solution(object):
    directions = range(4) #[0,1,2,3] right, down, left up
    bDebug = False
    def __init__(self):
        pass

    def printMatrix(self, matrix):
        """
        type: matrix , mXn list of lists
        output none
        description: print matrix
        """
        
        #print "\n".join( [ str((lambda l: [ (str(n)+", ") for n in l])(l) ) for l in matrix ] ) #breakdown below
        # "\n".join(list) will join \n (new line ) for each element in list (which looks like:["['0, ', '1, ', '2, ', '3, ']", "['0, ', '1, ', '2, ', '3, ']", "['0, ', '1, ', '2, ', '3, ']", "['0, ', '1, ', '2, ', '3, ']"]
        #  [ str((lambda l: [ (str(n)+", ") for n in l])(l) ) for l in matrix ]   nested list comprehension 
        #  outer runs on matrix lines
        #  inner defines and runs lambda that converts n in line to string and adds ","

        if matrix is None:
            print "Got None matrix"
            return

        for l in matrix:
            for n in l:
                print "{:>3},".format(n),
            print '\n',

    def generateMatrix(self, n):
        """
        :type n: int
        :rtype: List[List[int]]
        """
        distance = n #distance starts as n to go right, then n-1 down and left, then n-2 up and right and so on. stop cond. distance == 0

        matrix = [ [ 0 for i in range(n) ] for j in range(n) ]  # NxN 0 matrix, now matrix[i][j] will work within NxN boundary

        #directionsOperations= { 0 : lambda m,d,n: [m[for i in range(d)   #instead of switch case, use lambdas or functions dictionary. Hold that though. 
            #first do traditional if elif struct. 

        i,j = 0,0
        direction = 0
        numGen = genNumsToSquare(n)
        totalSet = 0
        while (totalSet < n*n):
            curDistance = distance
            if self.bDebug :
                print "i,j={0},{1}, dist={2}, totalSet={3}, n={4}".format(i,j, curDistance,totalSet,n) 

            while (  curDistance > 0):
                matrix[i][j] = next(numGen) 
                totalSet = totalSet +1
                if self.bDebug :
                    print "setting matrix[{0}][{1}]={2}. direction={5}, curDistance={3}, totalSet={4}".format(i,j,matrix[i][j], curDistance, totalSet,direction) 
                curDistance = curDistance -1

                if (direction == 0) : #right
                    if (curDistance == 0): #change direction and reduce distance
                        distance = distance -1 #next state, down, distance decreased by 1
                        i = i+1 #go down one raw
                    else: #walk right one column
                        j = j+1


                elif (direction == 1): #down
                    if (curDistance == 0): 
                        #going left has same distance as going down, so don't reduce distance
                        j = j-1 #walk left one column
                    else:
                        i = i+1


                elif (direction == 2): #left
                    if (curDistance == 0): #reduce distance
                        distance = distance -1 #next state, up, distance decreased by 1
                        i = i -1
                    else:
                        j = j-1

                elif (direction == 3): #up
                    if (curDistance == 0): 
                        #going right has same distance as going up, so don't reduce distance
                        j = j+1
                    else:
                        i = i-1

                if (curDistance == 0): #change direction 
                    direction = (direction +1 ) % 4 # the spiral order is always right,down,left,up (0-3)
                    break
            #while (  curDistance > 0):
        #while (totalSet < n):

        if self.bDebug :
            print "finished generating matrix" 
        return matrix



    def __del__(self):
        pass




        