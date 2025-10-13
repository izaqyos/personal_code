"""
Seating Arrangements
There are n guests attending a dinner party, numbered from 1 to n. The ith guest has a height of arr[i] inches.
The guests will sit down at a circular table which has n seats, numbered from 1 to n in clockwise order around the table. As the host, you will choose how to arrange the guests, one per seat. Note that there are n! possible permutations of seat assignments.
Once the guests have sat down, the awkwardness between a pair of guests sitting in adjacent seats is defined as the absolute difference between their two heights. Note that, because the table is circular, seats 1 and n are considered to be adjacent to one another, and that there are therefore n pairs of adjacent guests.
The overall awkwardness of the seating arrangement is then defined as the maximum awkwardness of any pair of adjacent guests. Determine the minimum possible overall awkwardness of any seating arrangement.
Signature
int minOverallAwkwardness(int[] arr)
Input
n is in the range [3, 1000].
Each height arr[i] is in the range [1, 1000].
Output
Return the minimum achievable overall awkwardness of any seating arrangement.
Example
n = 4
arr = [5, 10, 6, 8]
output = 4
If the guests sit down in the permutation [3, 1, 4, 2] in clockwise order around the table (having heights [6, 5, 8, 10], in that order), then the four awkwardnesses between pairs of adjacent guests will be |6-5| = 1, |5-8| = 3, |8-10| = 2, and |10-6| = 4, yielding an overall awkwardness of 4. It's impossible to achieve a smaller overall awkwardness.
"""
import math




def minOverallAwkwardness(arr):
    import sys
    def hsort(lst):
        import heapq
        h = []
        for elem in arr:
            heapq.heappush(h, elem) 
        return [ heapq.heappop(h) for x in  arr]

    #arr.sort() #ToDo, def heapsort  so as not to make it too easy
    arr = hsort(arr)
    
    #idea, sort so that height diff across adjacent guests is minimal.
    #problem are edges first and last elem will have the biggest awkwardness 
    # so we need to swap the first guest with another towards the middle so
    # that. the heigh diff between it and last and the first vs the next to the
    # right of the middle are miminal.
    # e.g. g0,g1,..,gj,gj+1,...gn  ascending. so that max(diff(gn,g0),
    # diff(gj,gj+1) ) is minimal
    #Try swap 0 and  jth elem. and calculate min max awkwardness
    j=1
    gmx=sys.maxsize
    while j<len(arr)-1: 
        arr[0], arr[j] = arr[j], arr[0]
        mx = max( abs(arr[len(arr)-1]-arr[0]), abs(arr[j+1]- arr[j]))
        #mx = 0
        #for i in range(len(arr)):
        #  j= (i+1)%(len(arr))
        #  if abs(arr[i]-arr[j]) > mx:
        #    mx= abs(arr[i]-arr[j])
        gmx = min( mx, gmx)
        arr[0], arr[j] = arr[j], arr[0]
        j+=1
    return gmx











# These are the tests we use to determine if the solution is correct.
# You can add your own at the bottom, but they are otherwise not editable!

def printInteger(n):
  print('[', n, ']', sep='', end='')

test_case_number = 1

def check(expected, output):
  global test_case_number
  result = False
  if expected == output:
    result = True
  rightTick = '\u2713'
  wrongTick = '\u2717'
  if result:
    print(rightTick, 'Test #', test_case_number, sep='')
  else:
    print(wrongTick, 'Test #', test_case_number, ': Expected ', sep='', end='')
    printInteger(expected)
    print(' Your output: ', end='')
    printInteger(output)
    print()
  test_case_number += 1

if __name__ == "__main__":
  arr_1 = [5, 10, 6, 8]
  expected_1 = 4
  output_1 = minOverallAwkwardness(arr_1)
  check(expected_1, output_1)

  arr_2 = [1, 2, 5, 3, 7]
  expected_2 = 4
  output_2 = minOverallAwkwardness(arr_2)
  check(expected_2, output_2)




