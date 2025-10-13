rows = int(input("Enter Hollow Square Star With Diagonals Rows = "))

print("Hollow Square Star With Diagonals Pattern") 

for i in range(rows):
    for j in range(rows):
        if(i == 0 or i == rows - 1 or j == 0 or j == rows - 1
           or i == j or j == (rows - 1 - i)):
            print('* ', end = '')
        else:
            print('  ', end = '')






