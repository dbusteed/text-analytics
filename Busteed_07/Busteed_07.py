# Davis Busteed -- LING 360 -- HW #7

# Instructions:
# In the CMS there is an untagged corpus named "AWE_untagd.zip". Write a Python program that 
# uses the default part-of-speech tagger in the NLTK library to tag the AWE corpus. Your 
# program should identify all noun + noun sequences (e.g., cell distribution, government 
# policy) where both nouns are common nouns (not proper nouns). Make sure to include
# both singular and plural nouns. For each of the six registers in the AWE corpus, generate 
# a normed rate of occurrence per 1,000 words for all noun + noun pairs. Your program should 
# then write 6 .csv files, one for each of the registers, with three columns: noun1, noun2,
# normed_freq, arranged in descending order by frequency (with the most frequency pair first). 

# With a small sample of the corpus (a file or two), check precision and recall of your program. 
# In a .docx file, write a report in which you interpret and compare the frequency of noun + noun 
# pairs across the six registers. Also, report the precision and recall measurements in the sample 
# of the corpus you chose.

import nltk
import os
import math
import re

PATH_TO_CORPUS = '../AWE_untagd'
NORMALIZE_COUNT = 1000
NOUNS = ['NN', 'NNS']

files = os.listdir(PATH_TO_CORPUS)

counts = {}

# loop thru the files (i/enumerate are just for progress bar)
for i, file_name in enumerate(files):

    # "progress bar" to notify user every 10% of completion 
    if i % (len(files) / 10) == 0 or i == len(files)-1:
        print('\rCompletion: {0}%'.format(math.ceil(( i / (len(files)/10) )*10)), end='')

    txt = open(os.path.join(PATH_TO_CORPUS, file_name), 'r').read().lower()
    txt = txt.split('<end header>')[1]

    reg_code = file_name[:5]

    if reg_code not in counts:
        counts[reg_code] = {'TOTAL_LEN': 0,}

    tokens = nltk.word_tokenize(txt)

    counts[reg_code]['TOTAL_LEN'] += len(tokens)

    tags = nltk.pos_tag(tokens)

    for i in range(0, len(tags)-1):
        
        if tags[i][1] in NOUNS and tags[i+1][1] in NOUNS:
            
            combo = '_'.join([ tags[i][0], tags[i+1][0] ])
            
            if combo not in counts[reg_code]:
                counts[reg_code][combo] = 1
            else:
                counts[reg_code][combo] += 1

for inner_dict in counts.values():

    total_len = inner_dict['TOTAL_LEN']
    
    # go thru each feature and count within that dictionary
    # and calculate the normilzed count
    for noun_combo, count in inner_dict.items():
        inner_dict[noun_combo] = round(count / total_len * NORMALIZE_COUNT, 2)
    
    # get rid of the length count (we don't want it in our summary)
    del inner_dict['TOTAL_LEN']

print('\n')

for reg_code, results in counts.items():

    counts[reg_code] = sorted(results.items(), key=lambda x:x[1], reverse=True)

    with open('dbl_noun_freq_' + reg_code + '.csv', 'w') as f:
        
        # CSV header
        f.write(f'{reg_code},\n\n')
        f.write(f'noun1,noun2,normed_freq\n')

        # loop thru the sorted tuples and write to file
        for combo_noun, freq in counts[reg_code]:

            nouns = combo_noun.split('_')

            f.write(f'{nouns[0]},{nouns[1]},{freq}\n')

    print(f'Freq list created for the {reg_code} register -- ({len(counts[reg_code])} different noun pairs found)')

# i just like an blank line for the console output
print()