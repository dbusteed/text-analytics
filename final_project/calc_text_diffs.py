from fuzzywuzzy import fuzz
from my_progressbar import start_pbar
from project_settings import CORPUS_PATH, CHAPTERS_IN_BIBLE, list_dir_by_time
from pandas import DataFrame
import os

version_diffs = {}

ver = os.listdir(CORPUS_PATH)

for j in range(0, len(ver)):
    for k in range(j+1, len(ver)):

        pbar, i = start_pbar(CHAPTERS_IN_BIBLE, f'Calculating diffs between {ver[j]} and {ver[k]} Bible')

        books_j = list_dir_by_time( os.path.join(CORPUS_PATH, ver[j]) )
        books_k = list_dir_by_time( os.path.join(CORPUS_PATH, ver[k]) )

        ver_combo = (ver[j], ver[k])

        # use tuple as key?
        version_diffs[ver_combo] = []

        for book_idx in range(0, len(books_j)):
            
            chaps_j = list_dir_by_time( books_j[book_idx] )
            chaps_k = list_dir_by_time( books_k[book_idx] )

            # version_diffs[ver_combo]

            for chap_idx in range(0, len(chaps_j)):
                
                # NEED TO FIX?
                # txt_j = open(chaps_j[chap_idx], 'r', encoding='utf8', errors='ignore').read()
                # txt_k = open(chaps_k[chap_idx], 'r', encoding='utf8', errors='ignore').read()
                txt_j = open(chaps_j[chap_idx], 'r', encoding="ISO-8859-1",).read()
                txt_k = open(chaps_k[chap_idx], 'r', encoding="ISO-8859-1",).read()

                version_diffs[ver_combo].append( fuzz.ratio(txt_j, txt_k) )

                pbar.update(i)
                i += 1

        pbar.finish()

print('\nFuzzy scores written out to a CSV\n')
DataFrame.from_dict(version_diffs).to_csv( os.path.join('other_data', 'fuzzy_scores.csv'), index=False)