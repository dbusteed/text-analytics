# Davis Busteed -- LING 360 -- HW5

# Instructions:
# Create a program that creates 8 separate word frequency lists, one for each of the 8 registers 
# in the Mini-CORE corpus, ordered in descending order of frequency, that is, with the highest 
# frequency first. Each frequency list (one per register) should be written to a separate .csv file. 
# The program should exclude stopwords from your frequency lists. Use either the stop-words 
# Python module or the stopword list in the NLTK library to exclude stopwords.

# import libraries
import os
import math
import re
from nltk.corpus import stopwords

# change this to your corpus location
PATH_TO_CORPUS = '..\mini_core'

# define a list of stop words, and add blank strings too
STOPWORDS = stopwords.words('english')
STOPWORDS.append('')

# main dict for tracking our counts
counts = {}

# get the file names from corpus
files = os.listdir(PATH_TO_CORPUS)

# loop thru the files (i/enumerate are just for progress bar)
for i, file_name in enumerate(files):

    # "progress bar" to notify user every 10% of completion 
    if i % (len(files) / 10) == 0 or i == len(files)-1:
        print('\rCompletion: {0}%'.format(math.ceil(( i / (len(files)/10) )*10)), end='')

    # read the file into memory
    txt = open(os.path.join(PATH_TO_CORPUS, file_name), 'r').read().lower()

    # remove the headers depending on which comes first
    # <h> or <p>, then split it there
    if txt.find('<h>') < txt.find('<p>'):
        txt = txt[txt.find('<h>'):]
    else:
        txt = txt[txt.find('<p>'):]

    # get the register code
    txt_code = file_name[2:4]

    # if this is the first time reading from
    # this register make a blank dict
    if txt_code not in counts:
        counts[txt_code] = {}

    # split the text into a list of tokens on the following characters
    tokens = re.split(r'[%\d:"\]\[\s+\.\?!,)(/-]|<[ph]>', txt)

    # remove the tokens that are considered stopwords
    tokens = [tok for tok in tokens if tok not in STOPWORDS]

    # look at each word
    for word in tokens:
        
        # if the word isn't in the dictionary yet, give it a count of 1,
        # if we've seen if already, then just add one to the count
        if word not in counts[txt_code]:
            counts[txt_code][word] = 1
        else:
            counts[txt_code][word] += 1
                
print('\n')

# go thru the dictionary, looking at the
# dictionary for each register 
for key, values in counts.items():

    # sort the inner dictionary by the count (descending) and store as list of tuples
    counts[key] = sorted(values.items(), key=lambda x:x[1], reverse=True)

    # make a new CSV file identified by the register code
    with open('word_freq_' + key + '.csv', 'w') as f:
        
        # CSV header
        f.write(f'{key},\n\n')
        f.write(f'word,frequency\n')

        # loop thru the sorted tuples and write to file
        for k,v in counts[key]:
            f.write(f'{k},{v}\n')

    # message for the user
    print(f'CSV frequency list created for the {key} register -- ({len(counts[key])} different words)')

# i just like an blank line for the console output
print()