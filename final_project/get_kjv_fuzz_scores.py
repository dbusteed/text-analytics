# Davis Busteed -- LING 360 -- Final Project

#-------------------------------------------------------------#
#                                                             #
#   OVERVIEW -- this script just simplies one dataframe       #
#               to a dataframe of only KJV data. This         #
#               was original just done in the REPL, but       #
#               the scirpt made it easy to do again           #
#                                                             #
#-------------------------------------------------------------#

# modules
from shared.project_settings import MISC_PATH
import pandas as pd
import os

# file paths
FUZZ_FILE = 'fuzzy_scores.csv'
INDEX_FILE = 'chapter_index.csv'
CHAP_OUT_FILE = 'kjv_fuzz_scores.csv'
BOOK_OUT_FILE = 'kjv_fuzz_scores_by_book.csv'

# get the fuzzy scores and the index
df = pd.read_csv(os.path.join(MISC_PATH, FUZZ_FILE))
index = pd.read_csv(os.path.join(MISC_PATH, INDEX_FILE))

# limit the fuzzy scores the only KJV ones
kjv = df[['ESV-KJV','KJV-NASB', 'KJV-NIV', 'KJV-NKJV', 'KJV-NLT']]

# join the fuzzies with the index
kjv_index = pd.DataFrame.merge(index, kjv, right_index=True, left_index=True)

# save this one to CSV
kjv_index.to_csv(os.path.join(MISC_PATH, CHAP_OUT_FILE), index=False)
print('\nFuzzy scores for KJV (by chapter) written out to a CSV\n')

# get a starting point of the different books
agg_params = {}
book_cols = list( kjv_index.columns[list(kjv_index.columns).index('ESV-KJV'):] )

# this agg_params if a Pandas things, allows for SQL-esque GROUP BYs
for b in book_cols:
    agg_params[b] = 'mean'

# create a new DF that is just avg. by each book
kjv_index_2 = kjv_index.groupby('book', sort=False).agg(agg_params)

# save this file
kjv_index_2.to_csv(os.path.join(MISC_PATH, BOOK_OUT_FILE), index=False)
print('\nFuzzy scores for KJV (by book) written out to a CSV\n')