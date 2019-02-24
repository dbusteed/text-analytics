# DAVIS BUSTEED -- LING 360 -- HW 3

# Instructions:
# Find two texts that are each at least 500 words in length. Try to find one text that is more formal 
# and one that is less formal. Create a Python program that produces normalized counts per 100 words 
# for the number of (a) subject pronouns, (b) contractions, and (c) modal verbs in each of the texts. 
# You should have six counts: (1) subject pronouns in formal text, (2) subject pronouns in informal 
# text, (3) contractions in formal text, (4) contractions in informal text, (5) modal verbs in formal 
# text, (6) modal verbs in informal text. Check both the precision and the recall of your program's 
# ability to correctly find these three linguistic features. Simply paste the texts into your .py file. 
# Interpret the results in 100-200 words. Turn into the CMS a zipped file (with the extension .zip) with your 
# .py file and a .docx file with your interpretation of the results in which you describe any differences 
# between the texts, as well as a report on the precision and recall of your program.

# import required functions from libraries
from re import split, search

# constant values
SUBJ_PRONOUNS = ['i', 'you', 'he', 'she', 'it', 'we', 'ye', 'they', 'what', 'who']
MODAL_VERBS = ['can', 'could', 'may', 'might', 'must', 'shall', 'should', 'will', 'would']
NORMALIZE_COUNT = 100

# this function uses a regex to check if a  
# word is a contraction or not
def is_contraction(w):
  if search(r'\b\w+[\'\u2019][^s ]\w*|\bit[\'\u2019]s', w):
    return True
  else: 
    return False

# read in the two files (make them lowercase now for simplicity)
formal_txt = open('formal.txt', 'r', encoding='utf8').read().lower()
informal_txt = open('informal.txt', 'r', encoding='utf8').read().lower()

# dictionary to be used to keep track of feature counts
results = {
  'formal_subj_pronoun': 0,
  'formal_contractions': 0,
  'formal_modal_verbs': 0,
  'informal_subj_pronoun': 0,
  'informal_contractions': 0,
  'informal_modal_verbs': 0,
}

# split up the text into a list of words (split on spaces, whitespace, and other punctuation)
formal_tokens = split(r'[\s+\.\?!,)(]', formal_txt)
informal_tokens = split(r'[\s+\.\?!,)(]', informal_txt)

# remove empty strings from the list of tokens
formal_tokens = [tok for tok in formal_tokens if tok != '']
informal_tokens = [tok for tok in informal_tokens if tok != '']

# loop thru the words in the formal txt
for word in formal_tokens:
  
  # check if the word is a subject pronoun from the list
  # if so, add one to the feature count
  if word in SUBJ_PRONOUNS:
    results['formal_subj_pronoun'] += 1
  
  # check if the word is a contraction
  if is_contraction(word):
    results['formal_contractions'] += 1

  # check if the word is a modal verb
  if word in MODAL_VERBS:
    results['formal_modal_verbs'] += 1

# do the same for the informal txt
for word in informal_tokens:

  if word in SUBJ_PRONOUNS:
    results['informal_subj_pronoun'] += 1
  
  if is_contraction(word):  
    results['informal_contractions'] += 1

  if word in MODAL_VERBS:
    results['informal_modal_verbs'] += 1

# loop the dictionary of results, calculate the normalized count
# and display the results
print(f'\nNormalized Counts per {NORMALIZE_COUNT} Words\n')

for key,value in results.items():
  if key[0] == 'f': 
    norm_val = value / len(formal_tokens) * NORMALIZE_COUNT
  else:
    norm_val = value / len(informal_tokens) * NORMALIZE_COUNT

  # add a space between the formal and informal results
  if(key == 'informal_subj_pronoun'):
    print('')

  # print the feature name and the normalized count (formatted nicely)
  print(f'{key.upper()}\t{norm_val:05.2f}')

print('\n')