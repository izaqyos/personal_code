#!/usr/local/bin/python3
import optparse

class optParser:
    def __init__(self):
        parser = optparse.OptionParser()

        parser.add_option('-n', '--new', help='creates a new object')
        parser.add_option('-b', help='boolean option', dest='bool', default=False, action='store_true')
        parser.add_option('-s', help='arguments', dest='str', action='store') 
        parser.add_option('-i', help='arguments', dest='int', action='store', type='int', default=10)
        (self.opts, self.args) = parser.parse_args()

    def __repr__(self):
        return 'opts: '+str(self.opts) + ', args: '+str(self.args)

    def __str__(self):
        return 'opts: '+str(self.opts) + ', args: '+str(self.args)

if __name__ == '__main__':
    optParser = optParser()
    print('optParser: {}'.format(optParser))
