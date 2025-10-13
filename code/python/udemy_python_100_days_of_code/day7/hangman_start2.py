#Step 1 

word_list = ["aardvark", "baboon", "camel"]

#TODO-1 - Randomly choose a word from the word_list and assign it to a variable called chosen_word.

#TODO-2 - Ask the user to guess a letter and assign their answer to a variable called guess. Make guess lowercase.

#TODO-3 - Check if the letter the user guessed (guess) is one of the letters in the chosen_word.
import random
word = random.choice(word_list)
char = input("Please select a character\n")[0].lower()
#if char in word:
#  print(f"your guess {char} is in {word}")

for i,c in enumerate(word):
  if c == char:
    print(f"found match for char {c} at index {i}")
  else:
    print("no match")
