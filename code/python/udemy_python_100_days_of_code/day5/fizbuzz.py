#Write your code below this row 👇
#like fizzbuzz game
# n%3 == 0 => fizz
# n%5 == 0 => buzz
# n%15 == 0 => fizzbuzz

fizz = "Fizz"
buzz = "Buzz"
for i in range(1,101):
    if i%15 == 0:
        print(fizz+buzz)
    elif i%5 == 0:
        print(buzz)
    elif i%3 == 0:
        print(fizz)
    else:
        print(i)
