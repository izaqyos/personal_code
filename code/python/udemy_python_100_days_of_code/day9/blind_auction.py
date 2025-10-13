from replit import clear
#HINT: You can call clear() to clear the output in the console.
#silent bid game

from art import logo
print(logo)
def silent_bid():
  bids={}
  ans="yes"
  while ans=="yes":
    print("Welcome to the secret auction program")
    name = input("what is your name?\n")
    bid = int(input("what is your bid?\n$"))
    bids[name]=bid
    ans = input("Type 'yes' to cont. or 'no' to stop bidding\n")
    clear()
    
  highest_bid, highest_bidder = float('-inf'), ""
  for k,v in bids.items():
    if v>highest_bid:
      highest_bid = v
      highest_bidder = k
  print(f"winner is {highest_bidder} with ${highest_bid} bid")

silent_bid()

