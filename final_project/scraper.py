# Davis Busteed -- LING 360 -- Final Project

from bs4 import BeautifulSoup as bs
from requests import get
import os

CORPUS_PATH = 'bible_versions'

# version codes and url snippets
booklist = {
    'KJV': 'King-James-Version-KJV-Bible',
    'ESV': 'English-Standard-Version-ESV-Bible',    
    'NASB': 'New-American-Standard-Bible-NASB',    
    'NLT': 'New-Living-Translation-NLT-Bible',    
    'NIV': 'New-International-Version-NIV-Bible',    
    'NKJV': 'New-King-James-Version-NKJV-Bible',    
}

version_chapters = {}

chapter_count = 0

for code, url_snippet in booklist.items():
    version_chapters[code] = []

    print(code)

    page = get(f'https://www.biblegateway.com/versions/{url_snippet}/#booklist').text
    ppage = bs(page, 'html.parser')

    table = ppage.find(class_='chapterlinks')
    rows = table.findAll('tr')

    for row in rows:
        book = row.find(class_='book-name')
        nums = book.find(class_='num-chapters').text
        name = book.text.replace(nums, '')

        chapter_count += int(nums)

        version_chapters[code].append([name, nums])



# ## STEP 2: Scrape and Save

# if not os.path.exists(CORPUS_PATH):
#     os.mkdir(CORPUS_PATH)

# for version, books in version_chapters.items():
#     # ex. version: 'KJV', books: [[Gen, 50], [Exo, 40]...]

#     if not os.path.exists(os.path.join(CORPUS_PATH, version)):
#         os.mkdir(os.path.join(CORPUS_PATH, version))

#     if(version == 'KJV'): # DEBUG
#         for book in books:
#             book_name = book[0]

#             if not os.path.exists(os.path.join(CORPUS_PATH, version, book_name)):
#                 os.mkdir(os.path.join(CORPUS_PATH, version, book_name))

#             for chapter in range(1,int(book[1])+1):
#                 print(f'Scraping {version} -- {book_name}-{chapter}')

#                 # with open(os.path.join(CORPUS_PATH, version, book_name, str(chapter)), 'w') as f:
#                     # f.write(f'Scraping {version} -- {book_name}-{chapter}')

#                 # page = get(f'https://www.biblegateway.com/passage/?search={book_name}+{chapter}&version={version}')
#                 # print(page) 