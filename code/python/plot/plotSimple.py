#!/usr/bin/python

import matplotlib.pyplot as plt

def genFibLst(n):
    rLst = [1,1]
    if n<2:
        return rLst[1,1]

    i=2 
    while i<n:
        rLst.append(rLst[i-2] + rLst[i-1])
        i+=1

    return rLst




plt.figure(1) 
plt.subplot(211)
plt.xlabel('X')
plt.text(10, 80, r'note x^2 curve')
plt.ylabel('Y=X**2')
plt.plot(range(20), [x**2 for x in range(20)], 'bo')
plt.subplot(212)
plt.xlabel('X')
plt.ylabel('Y=Fibonaci')
plt.plot(range(20), genFibLst(20), 'r--' )
plt.show()

#plt.plot([x**2 for x in range(20)])
#plt.ylabel('X**2')
#plt.show()
#
#plt.plot(genFibLst(20))
#plt.ylabel('Fib(20)')
#plt.show()

