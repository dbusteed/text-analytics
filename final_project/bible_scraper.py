# Davis Busteed -- LING 360 -- Final Project

#-------------------------------------------------------------#
#                                                             #
#   OVERVIEW -- this script will scrape and create a corpus   # 
#               of Bible texts from different translations    #
#               found online at biblegateway.com              #
#                                                             #
#-------------------------------------------------------------#

# required modules
from shared.project_settings import CORPUS_PATH, CHAPTERS_IN_BIBLE
from shared.my_progressbar import start_pbar
from bs4 import BeautifulSoup, element
from requests import get
import os
import re

#----------------------------------------------------#
#                                                    #
#   STEP 1 -- initial values                         #
#                                                    #
#----------------------------------------------------#

# version codes and url snippets
booklist_urls = {
    'KJV': 'King-James-Version-KJV-Bible',
    'ESV': 'English-Standard-Version-ESV-Bible',    
    'NASB': 'New-American-Standard-Bible-NASB',    
    'NLT': 'New-Living-Translation-NLT-Bible',    
    'NIV': 'New-International-Version-NIV-Bible',    
    'NKJV': 'New-King-James-Version-NKJV-Bible',    
}

# this dict will store the version code as the key
# and an array of book names and the number of chapters in the book
version_chapters = {}

#---------------------------------------------------------#
#                                                         #
#   STEP 2 -- scrape the summary pages for each version   #
#             to get a listing of each book within and    #
#             and the number of chapters in each book     #
#                                                         #
#---------------------------------------------------------#

# start a progress bar 
pbar, i = start_pbar(len(booklist_urls), 'finding number of chapters per book per version')

for code, url_snippet in booklist_urls.items():
    # ex. code --> 'KJV', url_snippet --> 'King-James-Version-KJV-Bible'
    
    version_chapters[code] = []

    # grab the page that lists the available books and chapters for the version
    page = get(f'https://www.biblegateway.com/versions/{url_snippet}/#booklist')
    ppage = BeautifulSoup(page.text, 'html.parser')

    # select the main table, and grab all the rows
    table = ppage.find(class_='chapterlinks')
    rows = table.findAll('tr')

    # loop thru the <tr> tags
    for row in rows:
        
        # parse out the book name and number of chapters
        book = row.find(class_='book-name')
        nums = book.find(class_='num-chapters').text
        name = book.text.replace(nums, '')

        # add the bookname and chapter count combo to the version list
        version_chapters[code].append([name, nums]) # ex. ['Genesis', '50']

    # update the progress bar after loop iteration
    pbar.update(i)
    i += 1

# this closes up the progress bar
pbar.finish()

#---------------------------------------------------------#
#                                                         #
#   STEP 3 -- create the corpus paths, scrape each page   #
#             (every chapter for each translation) and    #
#             write out each verse to a .txt file         #
#             (one .txt file per chapter)                 #
#                                                         #
#---------------------------------------------------------#

# create the base path if not already there
if not os.path.exists(CORPUS_PATH):
    os.mkdir(CORPUS_PATH)

# let the scraping begin!
for version, books in version_chapters.items():
    # ex. version --> 'KJV', books --> [[Gen, 50], [Exo, 40]...]

    # do a progress bar for each version
    pbar, i = start_pbar(CHAPTERS_IN_BIBLE, f'scraping text from {version} Bible')
    
    # create folder for this translation if not present
    if not os.path.exists(os.path.join(CORPUS_PATH, version)):
        os.mkdir(os.path.join(CORPUS_PATH, version))

    # go thru the books
    for book in books:
        # ex. book --> ['Genesis', 50]

        book_name = book[0]

        # The NIV version uses Song of Songs, change to make them all match
        if book_name == 'Song of Songs':
            book_name = 'Song of Solomon'

        # create the path
        if not os.path.exists(os.path.join(CORPUS_PATH, version, book_name)):
            os.mkdir(os.path.join(CORPUS_PATH, version, book_name))

        # incrament thru each chapter
        for chapter in range(1, int(book[1]) + 1):
            # ex. for Genesis, chapter --> [1 ... 50]

            # now that we know the book, chapter, and version, we can grab the page thru the query string
            page = get(f'https://www.biblegateway.com/passage/?search={book_name}+{chapter}&version={version}')
            ppage = BeautifulSoup(page.text, 'html.parser')

            # select the main div
            main = ppage.find(class_='text-html')

            # example path --> ./bible_version/KJV/Genesis/1.txt
            with open(os.path.join(CORPUS_PATH, version, book_name, str(chapter)+'.txt'), 'w', encoding='utf8') as f:

                # for chapters written in poetry form
                if main.findAll(class_='poetry'):

                    text = main.findAll(class_='text')

                    # sometimes the chapter has a title that we don't want
                    if text[1].find(class_='chapternum'):
                        text.pop(0)
                        
                    # for poetry ones, each chapter will just be one long string
                    verse = ''

                    # loop thru the stuff
                    for t in text:

                        # remove tags 
                        [s.extract() for s in t(class_=['crossreference','versenum','chapternum','footnote'])]

                        # depending on what we got, return the text
                        for tag in t:
                            if isinstance(tag, element.Tag):
                                verse += tag.text + ' '
                            else:
                                verse += tag + ' '

                    # clean up the verse string by removing big gaps, adding consistent spaces
                    verse = re.sub(r'\.', '. ', verse)
                    verse = re.sub(r'\s{2,}', ' ', verse)
                    verse = re.sub(r'(\s)(\W)(\s)', r'\2\3', verse)

                    f.write( verse )
                    f.write('\n')
                
                # for normal formated chapters
                else:
                    
                    # easiest to grab verse texts by first grabbing the superscripted verse numbers
                    # (first verse doesn't have a verse num, but is found with 'chapternum')
                    verse_nums = main.findAll(class_='chapternum')
                    verse_nums.extend( main.findAll(class_='versenum') )

                    for num in verse_nums:
                        # ex. num --> <sup class="versenum">2 </sup>

                        verse = ''

                        # find the parent of the superscript tag. look thru these tags and only return text
                        # that isn't tags (don't footnotes. etc.), one of the versions has text in a 'woj' 
                        # class, so this also handles that
                        for tag in num.parent:
                            if not isinstance(tag, element.Tag):
                                verse += tag
                            else:
                                if 'class' in tag.attrs:
                                    if 'woj' in tag.attrs['class']:
                                        for t in tag:
                                            if not isinstance(t, element.Tag):
                                                verse += t

                        # write the verse to the file seprate by new lines
                        f.write( verse )
                        f.write('\n')
            
            # update the bar
            pbar.update(i)
            i += 1

    # finish it off
    pbar.finish()