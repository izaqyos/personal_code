#!/usr/bin/python

import sys
from fractions import gcd

def mygcd(x,y):
    if (y == 0):
        return x
    else:
        return mygcd(y, x%y) #euclid gcd


def main():
    linesList = []
    
#get a list of nums from stdin
    for line in sys.stdin:
        print "got line {0}".format(line)
    	list = [int(elem) for elem in line.split()]   #convert list of chars that split generates into list of ints
        print "Converted num list: {0}".format(list)
    	linesList.append(list)

    for line in linesList:
        if not (len(line) == 0):
            for n in line:
                print "num= {0}".format(n)
            gcdN = line[0]
            for num in line[1:]:
                print "calling gcd of {0} , {1}".format(gcdN, num)
                gcdN = mygcd(gcdN,num)
            print "gcd of nums {0} is {1}".format(line, gcdN)

        #more consice
            print "using fractions gcd and reduce. gcd= {0}".format( reduce(gcd,line))

if __name__ == "__main__":
    main()

