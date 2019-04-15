from shared.project_settings import CORPUS_PATH, MISC_PATH
from shared.project_settings import CHAPTERS_IN_BIBLE, list_dir_by_time
from shared.my_progressbar import start_pbar
from textblob import TextBlob
from statistics import mean
import pandas as pd
import os

OUT_FILE = 'chapter_sentiments.csv'
version_sent = {}

for version in os.listdir(CORPUS_PATH):

    pbar, i = start_pbar(CHAPTERS_IN_BIBLE, f'Analyzing sentiment for each chapter in {version} Bible')

    version_sent[version] = []

    books = list_dir_by_time( os.path.join(CORPUS_PATH, version) )

    for book in books:

        chapters = list_dir_by_time( book )

        for chap in chapters:

            verse_scores = []
            txt = open(chap, 'r', encoding='utf8', errors='ignore').read()

            for verse in txt.split('\n'):

                verse_scores.append(TextBlob(verse).polarity)
            
            version_sent[version].append( mean(verse_scores) )

            pbar.update(i)
            i += 1

    pbar.finish()

df = pd.DataFrame.from_dict(version_sent)
index_df = pd.read_csv(os.path.join(MISC_PATH, 'chapter_index.csv'))

sents_with_index = pd.DataFrame.merge(index_df, df, left_index=True, right_index=True)
sents_with_index.to_csv(os.path.join(MISC_PATH, OUT_FILE), index=False )