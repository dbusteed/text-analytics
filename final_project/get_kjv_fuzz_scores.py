from shared.project_settings import MISC_PATH
import pandas as pd

import os

FUZZ_FILE = 'fuzzy_scores.csv'
INDEX_FILE = 'chapter_index.csv'
CHAP_OUT_FILE = 'kjv_fuzz_scores.csv'
BOOK_OUT_FILE = 'kjv_fuzz_scores_by_book.csv'

df = pd.read_csv(os.path.join(MISC_PATH, FUZZ_FILE))
index = pd.read_csv(os.path.join(MISC_PATH, INDEX_FILE))

kjv = df[['ESV-KJV','KJV-NASB', 'KJV-NIV', 'KJV-NKJV', 'KJV-NLT']]

kjv_index = pd.DataFrame.merge(index, kjv, right_index=True, left_index=True)

kjv_index.to_csv(os.path.join(MISC_PATH, CHAP_OUT_FILE), index=False)
print('\nFuzzy scores for KJV (by chapter) written out to a CSV\n')

agg_params = {}
book_cols = list( kjv_index.columns[list(kjv_index.columns).index('ESV-KJV'):] )

for b in book_cols:
    agg_params[b] = 'mean'

kjv_index_2 = kjv_index.groupby('book', sort=False).agg(agg_params)

kjv_index_2.to_csv(os.path.join(MISC_PATH, BOOK_OUT_FILE), index=False)
print('\nFuzzy scores for KJV (by book) written out to a CSV\n')