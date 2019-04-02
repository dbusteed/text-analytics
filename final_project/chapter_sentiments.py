from textblob import TextBlob
from my_progressbar import start_pbar
from project_settings import CORPUS_PATH, CHAPTERS_IN_BIBLE
import pandas as pd
import os

version_sent = {}

for version in os.listdir(CORPUS_PATH):

    pbar, i = start_pbar(CHAPTERS_IN_BIBLE, f'Analyzing sentiment for each chapter in {version} Bible')

    version_sent[version] = []

    books = os.listdir( os.path.join(CORPUS_PATH, version) )
    books = [os.path.join(CORPUS_PATH, version, b) for b in books]
    books.sort(key=lambda x: os.path.getmtime(x))

    for book in books:

        chapters = os.listdir( book ) # def this?
        chapters = [os.path.join(book, c) for c in chapters]
        chapters.sort(key=lambda x: os.path.getmtime(x))

        # sum or avg? verse or chap?

        for chap in chapters:

            chapter_total = 0
            txt = open(chap, 'r', encoding='utf8', errors='ignore').read()

            for verse in txt.split('\n'):

                chapter_total += TextBlob(verse).polarity
            
            version_sent[version].append(chapter_total)

            pbar.update(i)
            i += 1

    pbar.finish()

print('\nSentiments written out to a CSV\n')
pd.DataFrame.from_dict(version_sent).to_csv( os.path.join('other_data', 'chapter_sentiments.csv'), index=False)