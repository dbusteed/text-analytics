# DAVIS BUSTEED -- LING 360

# Instructions:
# Create a Python program that requests a singular noun from the user and prints to screen the plural 
# from of that noun. Use the website below or other resources to become more familiar with singular and 
# plural nouns in English. Do the best you can to account for as many of the irregular plural forms as you can, 
# but don't worry about getting every last irregular form. Turn into the CMS your .py file named with your 
# last name and the assignment number, for example, "Brown_01.py".
# http://www.myenglishpages.com/site_php_files/grammar-lesson-plurals.php
# Optional:
# Modify your program so that it also converts plural nouns into singular nouns and prints to screen.

# nouns with irregular plural forms
IRREGULAR_NOUNS = {
  'fish': 'fish',
  'sheep': 'sheep',
  'barracks': 'barracks',
  'foot':	'feet',
  'tooth':	'teeth',
  'goose': 'geese',
  'child':	'children',
  'man':	'men',
  'woman':	'women',
  'person':	'people',
  'mouse':	'mice',
  'deer': 'deer',
  'trout': 'trout',
  'shrimp': 'shrimp',
  'buffalo': 'buffalo',
  'die': 'dice',
  'ox': 'oxen',
  'moose': 'moose',
  'surf': 'surfs',
}

# nouns that end in 'o' that go to 'oes'
OES = [
  'echo',
  'embargo',
  'hero',
  'potato',
  'tomato',
  'torpedo',
  'veto'
]

# this function takes a singular noun
# and returns the plural form
def pluralize(n):
  
  # first check if it is an irregular noun, 
  # if so, return the corresponding plural form from the dictionary
  if n in IRREGULAR_NOUNS:
    n = IRREGULAR_NOUNS[n]
  
  # if not a irregular noun, check for the following patterns
  else:

    # words that end in 'ch', 'x', 's', 'z', or is 
    # in the special 'oes' nouns, add 'es' to the noun (box --> boxes)
    if n[-2:] == 'ch' or n[-1] in ['x', 's', 'z'] or n in OES:
      n += 'es'
    
    # words that end with a consonant + 'y' goes to 'ies' (baby --> babies)
    elif n[-1] == 'y' and n[-2] not in ['a', 'e', 'i', 'o', 'u']:
      n = n[:-1] + 'ies'
      
    # if ends in 'f', change to 'ves' (wolf --> wolves)
    elif n[-1] == 'f' and n[-2] != 'f':
      n = n[:-1] + 'ves'
      
    # words that end in 'fe' go to 'ves' (life --> lives)
    elif n[-2:] == 'fe' and n[-3] != 'f':
      n = n[:-2] + 'ves'
    
    # words that end in 'is' change to 'es' (analysis --> analyses)
    elif n[-2:] == 'is':
      n = n[:-2] + 'es'
    
    # for all other nouns, just add an 's' (dog --> dogs)
    else:
      n += 's'

  # return the new plural form!
  return n

# this function takes a plural noun
# and returns the singular form
def singularize(n):
  
  # first check if the word is a plural version of a singular word
  # in the list of irregular nouns (reverse dictionary lookup)
  if n in IRREGULAR_NOUNS.values():
    n = next(key for key, value in IRREGULAR_NOUNS.items() if value == n)

  # if not a irregular noun, check for the following patterns
  else:

    # if ends in and 'es' with a preceding 's', 'x', 'z', and 'ch',
    # or an 'es' and also in the OES special list, remove the 'es' (boxes --> box)
    if n[-2:] == 'es' and ((n[-3] in ['s', 'x', 'z'] or n[-4:-2] == 'ch') or (n[:-2] in OES )):
      n = n[:-2] 
    
    # if it ends in 'ies', remove the 'ies' and add 'y' (babies --> baby)
    elif n[-3:] == 'ies':
      n = n[:-3] + 'y'

    # for words ending in 'ves', remove the 'ves' and add 'f' or 'fe'
    # i think the alternative to this would be more additions to the IRREGULAR dictionary
    # and i thought this way would work ok (lives --> life) or (wolves --> wolf)
    elif n[-3:] == 'ves':
      n = n[:-3] + 'f or ' + n[:-3] + 'fe' 
    
    # for everything else, just remove the 's' (dogs --> dog)
    else:
      n = n[:-1]

  # return the new singular form!
  return n

# main loop of the program
print('\nNOUN PLURAL-IZER')

# this will continue to ask for singular and plural nouns from the user
# until they enter 'q'
while True:
  
  # print this simple menu and allow the user to enter their choice
  print('\nEnter (s) to convert singular to plural'
    + '\nEnter (p) to convert plural to singular'
    + '\nEnter (q) to quit')
  option = input('\n?: ').lower()

  # if they chose 'q', exit the program
  if option == 'q':
    break
  
  # if they chose 's' or 'p'
  elif option in ['s', 'p']:
    
    # this prevents script from breaking in case of bad user input
    try:

      # prompt the user for a word
      noun = input('\nWord to convert?: ')

      # if 's' was entered, call the 'pluralize' method, and show the user
      if option == 's':
        print(f'\nThe plural form of {noun.upper()} is {pluralize(noun).upper()}')
      
      # if 'p' was entered, call the 'singularize' method, and show the user
      else:
        print(f'\nThe singular form of {noun.upper()} is {singularize(noun).upper()}')

    # ignore errors and continue the loop
    except:
      pass

  # notify user if invalid option entered, continue the loop
  else:
    print("\n** Please enter an 's', 'p', or 'q' **")