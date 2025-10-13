import sys
import re

def main():
    arg1 = sys.argv[1]
    if arg1:
        match = re.match("\D*(\d+)",arg1)
        if match: 
            takt=int(match.group(1))
            if takt%2:
                print('Yosi team is on dev scenario duty on takt '+str(takt))
            else:
                print('Sergey team is on dev scenario duty on takt '+str(takt))
        else:
            print('could not detect takt number. ex: Takt02')
    else:
        print('Please provide takt name')

if __name__ == '__main__':
    main()
