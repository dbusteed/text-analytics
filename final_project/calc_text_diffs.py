# Davis Busteed -- LING 360 -- Final Project

#-------------------------------------------------------------#
#                                                             #
#   OVERVIEW -- this script uses fuzzywuzzy, a module         #
#               that uses Levenshtein Distance to calculate   #
#               the differences between strings. it will      #
#               find the diffs between the bible versions     #
#               and save the scores to a CSV to be analyzed   #
#                                                             #
#-------------------------------------------------------------#

# libraries
from shared.project_settings import CHAPTERS_IN_BIBLE, list_dir_by_time
from shared.project_settings import CORPUS_PATH, MISC_PATH
from shared.my_progressbar import start_pbar
from pandas import DataFrame
from fuzzywuzzy import fuzz
import os

# initial vars
OUT_FILE = 'fuzzy_scores.csv'
version_diffs = {}
ver = os.listdir(CORPUS_PATH)

# this loop will make the indexes to compare each version
# to every other version once (ex: 0-1, 0-2, 1-2)
for j in range(0, len(ver)):
    for k in range(j+1, len(ver)):

        # prog bar
        pbar, i = start_pbar(CHAPTERS_IN_BIBLE, f'Calculating diffs between {ver[j]} and {ver[k]} Bible')

        # j --> represents ver[k], the 'base' version
        # k --> represents ver[j], the 'compare' version
        # every version will be compared to every other version, 
        # and since fuzz.ratio(a,b) == fuzz.ratio(b,a), it doesn't
        # matter too much which is 'base' and which is 'compare'
        
        # get books for each version
        books_j = list_dir_by_time( os.path.join(CORPUS_PATH, ver[j]) )
        books_k = list_dir_by_time( os.path.join(CORPUS_PATH, ver[k]) )

        # ver_combo will act as the key in the dict/csv
        ver_combo = f'{ver[j]}-{ver[k]}'

        
        version_diffs[ver_combo] = []

        # for each book
        for book_idx in range(0, len(books_j)):
            
            # get all the chapters
            chaps_j = list_dir_by_time( books_j[book_idx] )
            chaps_k = list_dir_by_time( books_k[book_idx] )

            # go thru the chapters
            for chap_idx in range(0, len(chaps_j)):
                
                # read the chapters in
                # (these encodings might need to be made more robust)
                txt_j = open(chaps_j[chap_idx], 'r', encoding="ISO-8859-1",).read()
                txt_k = open(chaps_k[chap_idx], 'r', encoding="ISO-8859-1",).read()

                # compare the chapters, and save the score
                version_diffs[ver_combo].append( fuzz.ratio(txt_j, txt_k) )

                # update bar
                pbar.update(i)
                i += 1

        # end bar
        pbar.finish()

# save the output
DataFrame.from_dict(version_diffs).to_csv(os.path.join(MISC_PATH, OUT_FILE), index=False)
print('\nFuzzy scores written out to a CSV\n')