#!/opt/homebrew/bin/python3

#TODO: Create a letter using starting_letter.txt 
#for each name in invited_names.txt
#Replace the [name] placeholder with the actual name.
#Save the letters in the folder "ReadyToSend".
    
#Hint1: This method will help you: https://www.w3schools.com/python/ref_file_readlines.asp
    #Hint2: This method will also help you: https://www.w3schools.com/python/ref_string_replace.asp
        #Hint3: THis method will help you: https://www.w3schools.com/python/ref_string_strip.asp

def load_names():
    names = []
    with open('Input/Names/invited_names.txt') as namesfile:
        for line in namesfile:
            names.append(line.strip())
    return names

def load_template():
    with open('Input/Letters/starting_letter.txt') as templatefile:
        template = templatefile.read()
    return template

def main():
    email_file_prefix = 'Output/ReadyToSend/letter_for_'
    name_placeholder='[name]'
    template = load_template()
    names = load_names()
    #template = template.replace('[name]', 'Yosi')
    print(f"Email template is\n{template}")
    print(f"send list is\n{names}")
    for name in names:
        email_file_name = email_file_prefix+name
        with open(email_file_name, mode='w') as outfile:
            print(f"generating email in file {email_file_name}")
            outfile.write(template.replace(name_placeholder, name))
    print('complete')

if __name__ == '__main__':
    main()
