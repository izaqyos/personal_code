student_dict = {
    "student": ["Angela", "James", "Lily"],
    "score": [56, 76, 98]
}

# Looping through dictionaries:
for (key, value) in student_dict.items():
    #Access key and value
    pass

import pandas
student_data_frame = pandas.DataFrame(student_dict)

# Loop through rows of a data frame
for (index, row) in student_data_frame.iterrows():
    # Access index and row
    # Access row.student or row.score
    print(f"Access index and row example. index={index}, row={row}")
    print(f"Access row.student and row.score.  { row.student } and { row.score } ")

# Keyword Method with iterrows()
# {new_key:new_value for (index, row) in df.iterrows()}

# TODO 1. Create a dictionary in this format:
# {"A": "Alfa", "B": "Bravo"}
nato_df = pandas.read_csv('nato_phonetic_alphabet.csv')
nato_dict = {row.letter : row.code for idx, row in nato_df.iterrows() }
print(nato_dict)

#nato_dict = {row['letter'] : row['code'] for idx, row in nato_df.iterrows() }

# TODO 2. Create a list of the phonetic code words from a word that the user inputs.

def word_to_nato(word):
    if not isinstance(word, str):
        raise ValueError('Word must be a string')
    nato_list = [nato_dict[letter.upper()] for letter in word]
    return nato_list


not_complete = True
while not_complete:
    try:
        word = input('Enter a word: ')
        print(word_to_nato(word))
    except KeyError as e:
        print('Sorry, only letters in alphabet please')
    else:
        not_complete = False
