#!/usr/local/bin/python3

def test():
    list2D=[[1,2,3],[4,5,6],[8,9]]
    print("test ways to flatten a list of lists. one level deep") 

    import itertools
    #import functools
    import numpy
    import operator
    import perfplot
    itertoolsFlat = list(itertools.chain(*list2D))

    flatFuncs = {} 
    forForFlat =  lambda lst: [ elem for sublist in lst for elem in sublist ] 
    forForFlat.__name__ = 'forForFlat'
    flatFuncs['forForFlat'] = forForFlat

    sumFlat = lambda lst: sum(lst, [])
    sumFlat.__name__ == 'sumFlat'
    flatFuncs['sumFlat'] = sumFlat
    #reduceFlat = lambda lst: functoosls.reduce(operator.concat, lst, []) 
    #flatFuncs['reduceFlat'] = reduceFlat
    #reduceIconcatFlat = lambda lst: functools.reduce(operator.iconcat, lst, []) 
    #flatFuncs['reduceIconcatFlat'] = reduceIconcatFlat
    #itertoolsChainFlat = lambda lst: list(itertools.chain_from_iterable(lst))
    #flatFuncs['itertoolsChainFlat'] = itertoolsChainFlat
    numPyFlat = lambda lst: list(numpy.array(lst).flat)
    numPyFlat.__name__ = 'numPyFlat'
    flatFuncs['numPyFlat'] = numPyFlat
    numPyConcatFlat = lambda lst: list(numpy.concatenate(lst))
    numPyConcatFlat.__name__ = 'numPyConcatFlat'
    flatFuncs['numPyConcatFlat'] = numPyConcatFlat

    for k,v in flatFuncs.items():
        print('running function ', k)
        print('flat list: ', v(list2D))

    perfplot.show(
        setup=lambda n: [list(range(10))] * n,
        kernels=[ sumFlat, forForFlat, numPyFlat, numPyConcatFlat ],
        labels=["sumFlat", "forForFlat", "numPyFlat", "numPyConcatFlat"],
        n_range=[2**k for k in range(16)],
        logx=True,
        logy=True,
        xlabel='num lists'
        )
if __name__ == '__main__':
    test()


