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

# import libraries
import nltk, os, math, re

# some constant values
PATH_TO_CORPUS = '../AWE_untagd'
NORMALIZE_COUNT = 1000
COMMON_NOUNS = ['NN', 'NNS']

# get all the files
files = os.listdir(PATH_TO_CORPUS)

# empty dictionary for storing counts
counts = {}

# loop thru the files (i/enumerate are just for progress bar)
for i, file_name in enumerate(files):

    # "progress bar" to notify user every 10% of completion 
    if i % (len(files) / 10) == 0 or i == len(files)-1:
        print('\rCompletion: {0}%'.format(math.ceil(( i / (len(files)/10) )*10)), end='')

    # read the file into memory and get rid of the header
    txt = open(os.path.join(PATH_TO_CORPUS, file_name), 'r').read()
    txt = txt.split('<End Header>')[1]

    # first 5 chars identify the register
    reg_code = file_name[:5]

    # if first time seeing this register
    if reg_code not in counts:
        counts[reg_code] = {'TOTAL_LEN': 0}

    # split the txt into tokens and get rid of blanks and single letter 'nouns'
    tokens = re.split(r'[%\d:"\]\[;\s+\.\?!,)(/-]', txt)
    tokens = [tok for tok in tokens if len(tok) > 1] 
    
    # add up the length of these tokens so that 
    counts[reg_code]['TOTAL_LEN'] += len(tokens)

    # find the POS for each token
    tags = nltk.pos_tag(tokens)

    # lower case the words so that we can compare them.
    # this had to be done after the pos_tag(), so that it could
    # correctly identify proper nouns
    tags = [ (w.lower(), t) for (w, t) in tags ]

    # loop thru each of the tagged words 
    # (use a counter to select the i-th and i+1-th word)
    for i in range(0, len(tags)-1):
    
        # if the current and following word is tagged as a common noun
        if tags[i][1] in COMMON_NOUNS and tags[i+1][1] in COMMON_NOUNS:
            
            # combine the two nouns so that it can be used
            # as a key for the dictionary of counts
            combo = '_'.join([ tags[i][0], tags[i+1][0] ])
            
            # incrament the count for this noun pair
            if combo not in counts[reg_code]:
                counts[reg_code][combo] = 1
            else:
                counts[reg_code][combo] += 1

# after all the files have been read thru calculate norm count
for inner_dict in counts.values():

    total_len = inner_dict['TOTAL_LEN']
    
    # go thru each feature and count within that dictionary
    # and calculate the normilzed count
    for noun_combo, count in inner_dict.items():
        inner_dict[noun_combo] = round(count / total_len * NORMALIZE_COUNT, 2)
    
    # get rid of the length count (we don't want it in our summary)
    del inner_dict['TOTAL_LEN']

print('\n')

# loop thru the counts to sort and output to CSV
for reg_code, results in counts.items():

    # sort the freq list DESC
    counts[reg_code] = sorted(results.items(), key=lambda x:x[1], reverse=True)

    # create a new file (overwrite if existing)
    with open('noun_pair_freq_' + reg_code + '.csv', 'w') as f:
        
        # CSV header
        f.write(f'{reg_code},\n\n')
        f.write(f'noun1,noun2,normed_freq\n')

        # loop thru the sorted tuples and write to file
        for combo_noun, freq in counts[reg_code]:

            # split the nouns back into two seperate nouns
            nouns = combo_noun.split('_')

            # write the following to the csv
            f.write(f'{nouns[0]},{nouns[1]},{freq}\n')

    # notify the user of the new file
    print(f'Freq list created for the {reg_code} register -- ({len(counts[reg_code])} different noun pairs found)')

# i just like an blank line for the console output
print()