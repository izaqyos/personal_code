def psetarr(A): 
    if len(A)==0: 
        return [[]] 
    a=A[0] 
    #print('split to {} and {}'.format(A[0], A[1:]))
    pset1n = psetarr(A[1:]) 
    #print('pset1n', pset1n)
    psetwithA = [] 
    for s in pset1n: 
        #print('appen {} w {}'.format([a], s))
        psetwithA.append([a] + s) 
        #print('psetwithA', psetwithA)
    return pset1n + psetwithA 

def test():
    inputs = [ [], [1], [1,2,3] ]
    expected = [ [], [[], [1]], [[],[1], [2],[3], [1,2,3], [1,2], [1,3], [2,3]] ]
    for inp in inputs:
       print('power set of', inp)
       out = psetarr(inp)
       print('result', out)
       #for i,o in zip(inputs,expected):
       #    r = psetarr(i)
       #    assert(r == o)


if __name__ == '__main__':
     test()
