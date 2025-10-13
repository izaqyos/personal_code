
def digit_freq(d, num):
    freq = 0
    while num>0:
        ld = num%10
        num//=10
        if d == ld:
            freq+=1
    return freq

def digit_frequencies(n):
    if n<=0:
        print('{} is negative or zero'.format(n))
        return
    maxdigit=-1
    maxfreq=0
    for d in range(10):
        dfreq = digit_freq(d, n)
        print('digit {} occurs {} time in {}'.format(d, dfreq, n))
        if dfreq > maxfreq:
            maxfreq = dfreq
            maxdigit = d
    print('digit {} occurs maximum number of time: {} in {}'.format(maxdigit, maxfreq, n))

def main():
    num = int(input('Please enter a positive number\n'))
    digit_frequencies(num)


def test():
    inputs = [0, 4, 444, 3232122556, 9977432222]
    for inp in inputs:
        print('-'*30)
        digit_frequencies(inp)
        print('-'*30)

if __name__ == "__main__":
    #test()
    main()
