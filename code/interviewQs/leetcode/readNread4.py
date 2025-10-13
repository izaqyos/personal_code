"""
The API: int read4(char *buf) reads 4 characters at a time from a file.

The return value is the actual number of characters read. For example, it returns 3 if there is only 3 characters left in the file.

By using the read4 API, implement the function int read(char *buf, int n) that reads n characters from the file.

Note:

The read function may be called multiple times.
"""

class Solution:
    def __init__(self, filename):
        self.file = open(filename, 'rb')

    def read4(self, buf):
        buf.clear()
        buf.extend(self.file.read(4))

    def readn(self, n):
        buf = []
        totalread = 0
        while totalread<= n-4:
            #print(totalread)
            self.read4(buf)
            #print('read ',len(buf))
            if not buf:
                #print('eof found. read so far ',totalread) 
                break
            totalread+=len(buf)
        return totalread



def test():
    files = ['temp', 'readNread4.py', 'LIS.py']
    readsizes = [20, 1000, 10000]
    for f,n in zip(files, readsizes):
        sol = Solution(f)
        totalread = sol.readn(n)
        print('{} read({}) has read {} chars'.format(f, n, totalread))

if __name__ == "__main__":
    test()


