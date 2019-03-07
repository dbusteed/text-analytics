# Davis Busteed -- LING 360 -- Final Project

from bs4 import BeautifulSoup as bs
from requests import get
import progressbar as pb
import os
from time import sleep

CORPUS_PATH = 'bible_versions'
PBAR_DISPLAY = [pb.Percentage(), ' ', pb.Bar(marker='*', left='[', right=']'), ' ', pb.Timer()]

# version codes and url snippets
booklist = {
    'KJV': 'King-James-Version-KJV-Bible',
    'ESV': 'English-Standard-Version-ESV-Bible',    
    'NASB': 'New-American-Standard-Bible-NASB',    
    'NLT': 'New-Living-Translation-NLT-Bible',    
    'NIV': 'New-International-Version-NIV-Bible',    
    'NKJV': 'New-King-James-Version-NKJV-Bible',    
}

# progress bar
i = 0
pbar = 0

def start_pbar(max_val, msg='processing'):
    global i, pbar
    i = 0
    print(f'\n{msg}\n')
    pbar = pb.ProgressBar(widgets=PBAR_DISPLAY, max_value=max_val, iterator=i)
    pbar.start()

version_chapters = {}

chapter_count = 0

# start_pbar(len(booklist), 'finding number of chapters per book per version')

# for code, url_snippet in booklist.items():
#     version_chapters[code] = []

#     page = get(f'https://www.biblegateway.com/versions/{url_snippet}/#booklist').text
#     ppage = bs(page, 'html.parser')

#     table = ppage.find(class_='chapterlinks')
#     rows = table.findAll('tr')

#     for row in rows:
#         book = row.find(class_='book-name')
#         nums = book.find(class_='num-chapters').text
#         name = book.text.replace(nums, '')

#         chapter_count += int(nums)

#         version_chapters[code].append([name, nums])

#     pbar.update(i)
#     i += 1

# pbar.finish()

## STEP 2: Scrape and Save

if not os.path.exists(CORPUS_PATH):
    os.mkdir(CORPUS_PATH)

start_pbar(chapter_count, 'scraping Bible text for each chapter for each book for each version\n(this might take a while)')

version_chapters = { # DEBUG
    'KJV': [['Genesis', '10']],
    'ESV': [['Genesis', '10']],
    'NASB': [['Genesis', '10']],
    'NLT': [['Genesis', '10']],
    'NIV': [['Genesis', '10']],
    'NKJV': [['Genesis', '10']],
}

for version, books in version_chapters.items():
    # ex. version: 'KJV', books: [[Gen, 50], [Exo, 40]...]

    if not os.path.exists(os.path.join(CORPUS_PATH, version)):
        os.mkdir(os.path.join(CORPUS_PATH, version))

    # if(version == 'KJV'): # DEBUG
    for book in books:
        book_name = book[0]

        if not os.path.exists(os.path.join(CORPUS_PATH, version, book_name)):
            os.mkdir(os.path.join(CORPUS_PATH, version, book_name))

        for chapter in range(1,int(book[1])+1):
            # print(f'Scraping {version} -- {book_name}-{chapter}')

            # with open(os.path.join(CORPUS_PATH, version, book_name, str(chapter)), 'w') as f:
                # f.write(f'Scraping {version} -- {book_name}-{chapter}')

            # page = get(f'https://www.biblegateway.com/passage/?search={book_name}+{chapter}&version={version}')
            # print(page)

            #  c = [t for t in sups[0].parent if not isinstance(t, bs4.element.Tag) ]

            sleep(.00001)
                            
            pbar.update(i)
            i += 1
    
pbar.finish()