
def sqrroot(n):
    odds = [ _ for _ in range(n) if _%2!=0]
    sumodds = 0
    numodds = 0
    for odd in odds:
        sumodds += odd
        numodds +=1
        if sumodds == n:
            return numodds
        if sumodds > n:
            print('{} has no integer square'.format(n))
            return 0
    return 0


def main():
    val = input("please enter positive number: ")
    val = int(val)
    sqr=sqrroot(val)
    print('square root of {} is {}'.format(val, sqr))

if __name__ == "__main__":
    main()
