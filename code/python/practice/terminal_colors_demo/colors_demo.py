#!/usr/local/bin/python3

"""
Demo of printing in color in terminal.
resource https://stackoverflow.com/questions/287871/print-in-terminal-with-colors
"""
from colorama import Fore, Back, Style

class bcolors:
    MAGENTA = '\033[96m'
    ORANGE = '\033[98m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'




def colorsGen():
        mColorList = ['OKBLUE', 'OKGREEN', 'HEADER', 'ORANGE', 'MAGENTA']
        mCurColorIdx=0 #for round robing
        rRobinVal=len(mColorList)
        while True:
            yield  mColorList[mCurColorIdx]
            mCurColorIdx = (mCurColorIdx +1) % rRobinVal

def colorsGenColorama():
        colorama=['BLACK', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE', 'GREEN', 'RED', 'RESET']
        mCurColorIdx=0 #for round robing
        rRobinVal=7
        while True:
            #print("color list={0}, index={1}, selected={2}".format(colorama, mCurColorIdx, colorama[mCurColorIdx]))
            yield  colorama[mCurColorIdx]
            mCurColorIdx = (mCurColorIdx +1) % rRobinVal

def runtTest1():
    print("Printing few colors");
    bcolorsInstance = bcolors()
    print("dir(bcolors)={0}".format(dir(bcolors)) )
    print("vars(bcolors)={0}".format(vars(bcolors)))
    bcolorsMembers=[attr for attr in dir(bcolors) if not attr.startswith("__")]
    print("bcolors members: {0}".format(bcolorsMembers))
    #map( lambda color:print(bcolors.color + " color " + bcolors.ENDC), bcolorsMembers) 
    for clr in bcolorsMembers:
        print(getattr(bcolors,clr) + clr  + bcolors.ENDC)

def print_format_table():
    """
    prints table of formatted text format options
    """
    for style in range(8):
        for fg in range(30,38):
            s1 = ''
            for bg in range(40,48):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
            print(s1)
        print('\n')

def printRRobinColoroma():
    gen = colorsGenColorama()
    for i in range(10):
        clr = next(gen)
        print(getattr(Fore,clr) + clr  + Fore.RESET)


def printRRobinColors():
    gen = colorsGen()
    for i in range(10):
        clr = next(gen)
        print(getattr(bcolors,clr) + clr  + bcolors.ENDC)


def runtTest2():
    print("Printing all colors and formats");
    print_format_table()

def runtTest3():
    print("Printing Colorama colors. round robin");
    printRRobinColoroma()

def runtTest4():
    print("Printing colors. round robin");
    printRRobinColors()

def runTests():
    runtTest1()
    runtTest2()
    runtTest3()
    runtTest4()

def main():
    runTests()

if __name__ == "__main__":
    main()
