#!/usr/local/bin/python3

class myHash:
    
    def __init__(self, size):
        self.storage = [None] * size

    def hashKey(self, key):
        return key%len(self.storage) 

    def insertNaive(self, key, val):
        self.storage[self.hashKey(key)] = val

    def getKeyNaive(self, key):
        return self.storage[self.hashKey(key)]

#open addressing, linear probing
    def insertOALP(self, key, val):
        index = self.hashKey(key)
        while storage[index] == None:
            index = (index +1) % len(self.storage) 
        self.storage[self.hashKey(key)] = val

    def getKeyOALP(self, key):
        index = self.hashKey(key)
        while storage[index] != key:
            index = (index +1) % len(self.storage) 
            if (storage[index] == None) or ( index == self.hashKey(key)) :
                return None
        return self.storage[index]


def test1():
    simpleHash = myHash(20)
    for i in range(10):
        simpleHash.insertNaive(i, i**2)
        print('key={}, val={}'.format(i, simpleHash.getKeyNaive(i)))


if __name__ == '__main__':
    test1()
