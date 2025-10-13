import timeit

my_list = [i for i in range(100000)]

def reverse_using_reverse():
    my_list.reverse()
    for item in my_list:
        pass

def reverse_using_reversed():
    for item in reversed(my_list):
        pass

def reverse_using_range():
    for i in range(len(my_list)-1, -1, -1):
        item = my_list[i]

def reverse_using_while():
    i = len(my_list) - 1
    while i >= 0:
        item = my_list[i]
        i -= 1

print('reverse_using_reverse:', timeit.timeit(reverse_using_reverse, number=1000))
print('reverse_using_reversed:', timeit.timeit(reverse_using_reversed, number=1000))
print('reverse_using_range:', timeit.timeit(reverse_using_range, number=1000))
print('reverse_using_while:', timeit.timeit(reverse_using_while, number=1000))

