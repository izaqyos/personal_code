class BITree:
    def __init__(self, numbers):
        self.numbers = [_ for _ in numbers] #make a copy
        self.size = len(numbers)
        self.bit = [0 for _ in range(self.size+1)] #0 index is dummy
        self.construct()

    def construct(self):
        #o(nlogn)
        for i,n in enumerate(self.numbers): 
            #print(f"updating value {n} at index {i} in BIT")
            self.updateSum(i,n) #o(logn)


    def updateValue(self, index, value):
        addedSumToBIT = value-self.numbers[index]
        self.numbers[index] = value
        #print(f"updating value {addedSumToBIT} at original index {index} in BIT")
        self.updateSum(index, addedSumToBIT)

    def updateSum(self, index, value):
        index+=1
        while index<=self.size:
            #print(f"updating sum at index {index} adding value {value}")
            self.bit[index]+=value
            index +=index&(-index) #bitwise operation n&-n leaves last set bit, add it to index to get it's parent in bittree 

    def getSumPrefix(self, right):
        retsum , index = 0, right+1
        while (index>0):
            retsum += self.bit[index]
            index -= index&(-index) #travel to parents in sum view of bittree by removing last set bit. idea is each node in bit keeps sum of certain range corressponding to a power of 2  representation of the index.
            #say index 11=8+2+1 so in node 11 is last value in this range, in node 10 last 2 sum and node 8 first eight values sum
        #print(f"sum in range 0 to {right} is retsum")
        return retsum

    def getSum(self, left, right):
        return self.getSumPrefix(right) - self.getSumPrefix(left-1)

    def printMe(self):
        print("indices row and numbers row are")
        for i in range(self.size):
            print(f"{i:<3d}", end='')
        print('')
        for n in self.numbers:
            print(f"{n:<3d}", end='')
        print('')

        print("BITree node indices and values rows are")
        for i in range(self.size + 1):
            print(f"{i:<3d}", end='')
        print('')
        for n in self.bit:
            print(f"{n:<3d}", end='')
        print('')


def test():
    testArrays = [
            [2, 1, 1, 3, 2, 3, 4, 5, 6, 7, 8, 9],
            [1,2,3,4,5,6,7],
            [4,9,3,2,11]
            ]
    #0 - sum operation followed by left and right indices
    #1 - update operation followed by index and value
    operations = [
            [[0,0,5], [1,3,9], [0,0,5]],
            [[0,0,2], [1,1,3], [0,0,2], [0,0,6]],
            [[0,0,2], [1,3,7], [0,0,2], [0,0,4]]
            ]
    for i,numbers in enumerate(testArrays):
        bitree = BITree(numbers)
        #bitree.printMe()
        for op in operations[i]:
            if op[0] == 0:
                retsum = bitree.getSum(op[1],op[2])
                bitree.printMe()
                print(f"sum in range {op[1]}-{op[2]} inclusive is {retsum}")
            elif op[0] ==1:
                bitree.updateValue(op[1],op[2])
                #bitree.updateSum(op[1],op[2]-numbers[op[1]])
                #bitree.printMe()
            else:
                print('illegal operation', op[0])

def main():
    test()

if __name__ == "__main__":
    main()
