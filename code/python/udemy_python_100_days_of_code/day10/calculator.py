from art import logo

def add(n1,n2):
  return n1+n2
def mult(n1,n2):
  return n1*n2
def div(n1,n2):
  return n1/n2
def sub(n1,n2):
  return n1-n2
  
def calc():
  ops = {
    '+': add,
    '-': sub,
    '/': div,
    '*': mult
  }

  n1 = float(input('Please insert first number: '))
  while True:
    n2 = float(input('Please insert next number: '))
    for op in ops:
      print(op)
    op = input("please choose operation from list above: ")
    n1 = ops[op](n1, n2)
    print(f"result is {n1}")
    ans = input(f"Type 'y' to continue with {n1}, 'n' to exit ")
    if ans!='y':
      break

print(logo)
calc()
