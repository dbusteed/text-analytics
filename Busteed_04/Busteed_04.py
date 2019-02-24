# Davis Busteed -- LING 360 -- HW #4

# NOTE: I didn't zip up the mini-core documents, so if you wanna
# run this you'll need to change PATH_TO_CORPUS

# import libraries
import os
import re
import math
import pandas as pd

# I/O values
PATH_TO_CORPUS = '..\mini_core'
OUT_FILE = 'results.csv'

# features to look for. these are defined as constants so that
# it's easier to try different features. just change this name
# and change the expression in the code
FEAT_1 = 'contractions'
FEAT_2 = 'possessive pronouns'
FEAT_3 = 'question marks'

# other constants
NORMALIZE_COUNT = 1000
POSS_PRONOUNS = ['my', 'mine', 'yours', 'your', 'his', 'hers', 'its', 'our', 'ours', 'theirs', 'their']

# empty dictionary 
results = {}

# get a list of all the files
files = os.listdir(PATH_TO_CORPUS)

# go thru each file in the list (the i/enumerate is just for the progress display)
for i, file_name in enumerate(files):

    # for every 10%, print to the console (kinda like a progress bar)
    if i % 160 == 0 or i == len(files)-1:
        print('\rCompletion: {0}%'.format(math.ceil((i/160)*10)), end='')

    # save the current file as a variable
    txt = open(os.path.join(PATH_TO_CORPUS, file_name), 'r').read().lower()

    # get rid of the header: if the <h> comes first, 
    # split it there, if the <p> comes first, split there
    if txt.find('<h>') < txt.find('<p>'):
        txt = txt[txt.find('<h>'):]
    else:
        txt = txt[txt.find('<p>'):]

    # get the register code from the file name
    txt_code = file_name[2:4]

    # if this is the first time seeing this register code
    # make a dictionary inside the dictionary with empty feature counts
    if txt_code not in results:
        results[txt_code] = {'TOTAL_LEN': 0, FEAT_1: 0, FEAT_2: 0, FEAT_3: 0}

    # split the text into tokens and remove the white spaces
    tokens = re.split(r'[\s+\.\?!,)(]|<[ph]>', txt)
    tokens = [tok for tok in tokens if tok != '']

    # keep track of the total length for each register
    results[txt_code]['TOTAL_LEN'] += len(tokens)

    # loop thru each word of the text to check for FEAT 1 and 2
    for word in tokens:
        
        # FEAT_1 -- check for contractions
        if re.search(r'\b\w+[\'\u2019][^s ]\w*|\bit[\'\u2019]s', word):
            results[txt_code][FEAT_1] += 1

        # FEAT_2 -- check from possessive pronouns
        if word in POSS_PRONOUNS:
            results[txt_code][FEAT_2] += 1

    # FEAT_3 -- check for question marks. since i split on
    # ?s earlier, this checks for ?s in from the raw txt
    results[txt_code][FEAT_3] += len(re.findall(r'\?', txt))


# now that all files have been processed
# go thru the dictionary for each register
for inner_dict in results.values():

    total_len = inner_dict['TOTAL_LEN']
    
    # go thru each feature and count within that dictionary
    # and calculate the normilzed count
    for feat, count in inner_dict.items():
        inner_dict[feat] = round(count / total_len * NORMALIZE_COUNT, 2)
    
    # get rid of the length count (we don't want it in our summary)
    del inner_dict['TOTAL_LEN']

# convert the dictionary of results to a Pandas DataFrame
# and save it as a CSV file
pd.DataFrame.from_dict(results, orient='index').to_csv(OUT_FILE)

print(f'\n\nResults written to {OUT_FILE}\n')