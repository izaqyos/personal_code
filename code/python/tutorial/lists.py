#!/usr/local/bin/python3

from random import randint
print('demo lists common ops')


print('lists generation')

empty_lst = []
rand_lst = [ randint(0,100) for x in range(20) ]
mat3x4 = [ [ i for i in range(4) ] for j in range(3) ]

print('rand_lst= ', rand_lst)
print('mat3x4= ', mat3x4)


print('lists slices')
print('shallow copy rand_lst= ', rand_lst[:])
print('prefix copy rand_lst= ', rand_lst[:-5])
print('suffix copy rand_lst= ', rand_lst[5:])
print(' copy every 3rd jump elem rand_lst= ', rand_lst[::3])
print(' reverse rand_lst= ', rand_lst[::-1])

print('lists addition')
rand_lst.append(90)
rand_lst.insert(0,90)
rand_lst.extend( [ 1,1,1])
print('rand_lst= ', rand_lst)
