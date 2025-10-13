#If the bill was $150.00, split between 5 people, with 12% tip. 

#Each person should pay (150.00 / 5) * 1.12 = 33.6
#Format the result to 2 decimal places = 33.60

#Tip: There are 2 ways to round a number. You might have to do some Googling to solve this.💪

#Write your code below this line 👇
def calculate_tip():
  bill = input("Please provide the total bill. ")
  add_dolar = False
  if bill[0] == '$':
    add_dolar = True
    bill = bill[1:]
    
  bill = float(bill)
  tip = float(input("what precentage of tip you'd like to pay? 10, 12, 15 etc... "))
  ppl = int(input("how many people to split the bill? "))
  amount_to_pay = bill*((100+tip)/100)
  if add_dolar:
    amount_to_pay = "$"+str(amount_to_pay)
  print(f"Each person should pay: {round(float(amount_to_pay)/ppl,2):.2f}")

calculate_tip()
