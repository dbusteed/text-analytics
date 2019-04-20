# Davis Busteed -- LING 360 -- Final Project

#---------------------------------------------------------------#
#                                                               #
#   OVERVIEW -- this calculates the sentiments for each chapter #
#                                                               #
#---------------------------------------------------------------#

# libs
from shared.project_settings import CORPUS_PATH, MISC_PATH
from shared.project_settings import CHAPTERS_IN_BIBLE, list_dir_by_time
from shared.my_progressbar import start_pbar
from textblob import TextBlob
from statistics import mean
import pandas as pd
import os

# init vars
OUT_FILE = 'chapter_sentiments.csv'
version_sent = {}

# for each version
for version in os.listdir(CORPUS_PATH):

    # prog bar for each version
    pbar, i = start_pbar(CHAPTERS_IN_BIBLE, f'Analyzing sentiment for each chapter in {version} Bible')

    # empty list for each version
    version_sent[version] = []

    # get books
    books = list_dir_by_time( os.path.join(CORPUS_PATH, version) )

    # go thru books
    for book in books:

        # get chapters then loop thru
        chapters = list_dir_by_time( book )

        for chap in chapters:

            # verse scores will be a list
            verse_scores = []

            # read the text in
            txt = open(chap, 'r', encoding='utf8', errors='ignore').read()

            # for each verse calc the sentiment
            for verse in txt.split('\n'):
                verse_scores.append(TextBlob(verse).polarity)
            
            # get the mean of the chapter and save it
            version_sent[version].append( mean(verse_scores) )

            # handle the bar
            pbar.update(i)
            i += 1

    pbar.finish()

# save the dictionary, and bring in the index DF
df = pd.DataFrame.from_dict(version_sent)
index_df = pd.read_csv(os.path.join(MISC_PATH, 'chapter_index.csv'))

# merge the index with the data, and save it to CSV
sents_with_index = pd.DataFrame.merge(index_df, df, left_index=True, right_index=True)
sents_with_index.to_csv(os.path.join(MISC_PATH, OUT_FILE), index=False )