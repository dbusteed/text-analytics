# Davis Busteed -- LING 360 -- Final Project

#-------------------------------------------------------------#
#                                                             #
#   OVERVIEW -- this script will scrape and create a corpus   # 
#               of Bible texts from different translations    #
#               found online at biblegateway.com              #
#                                                             #
#-------------------------------------------------------------#

# required modules
from bs4 import BeautifulSoup, element
from requests import get
import progressbar as pb
import os

#----------------------------------------------------#
#                                                    #
#   STEP 1 -- initial values, constants, functions   #
#                                                    #
#----------------------------------------------------#

CORPUS_PATH = 'bible_versions'
CHAPTERS_IN_BIBLE = 1189
PBAR_DISPLAY = [pb.Percentage(), ' ', pb.Bar(marker='*', left='[', right=']'), ' ', pb.Timer()]

# used to handle / format multiple uses of progress bar
def start_pbar(max_val, msg='processing'):
    
    # use the existing vars on the outside 
    # in running the progress bar
    global i, pbar
    
    i = 0
    print(f'\n{msg}\n')

    # inti the pbar and start
    pbar = pb.ProgressBar(widgets=PBAR_DISPLAY, max_value=max_val, iterator=i)
    pbar.start()

# version codes and url snippets
booklist = {
    'KJV': 'King-James-Version-KJV-Bible',
    'ESV': 'English-Standard-Version-ESV-Bible',    
    'NASB': 'New-American-Standard-Bible-NASB',    
    'NLT': 'New-Living-Translation-NLT-Bible',    
    'NIV': 'New-International-Version-NIV-Bible',    
    'NKJV': 'New-King-James-Version-NKJV-Bible',    
}

# initial progress bar values
i = 0
pbar = 0

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
start_pbar(len(booklist), 'finding number of chapters per book per version')

for code, url_snippet in booklist.items():
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
    start_pbar(CHAPTERS_IN_BIBLE, f'scraping text from {version} Bible')
    
    # create folder for this translation if not present
    if not os.path.exists(os.path.join(CORPUS_PATH, version)):
        os.mkdir(os.path.join(CORPUS_PATH, version))

    # go thru the books
    for book in books:
        # ex. book --> ['Genesis', 50]

        book_name = book[0]

        # create the path
        if not os.path.exists(os.path.join(CORPUS_PATH, version, book_name)):
            os.mkdir(os.path.join(CORPUS_PATH, version, book_name))

        # incrament thru each chapter
        for chapter in range(1, int(book[1]) + 1):
            # ex. for Genesis, chapter --> 1 ... 50

            # now that we know the book, chapter, and version, we can grab the page thru the query string
            page = get(f'https://www.biblegateway.com/passage/?search={book_name}+{chapter}&version={version}')
            ppage = BeautifulSoup(page.text, 'html.parser')
            
            # select the main div
            main = ppage.find(class_='text-html')

            # easiest to grab verse texts by first grabbing the superscripted verse numbers
            # (first verse doesn't have a verse num, but is found with 'chapternum')
            verse_nums = main.findAll(class_='chapternum')
            verse_nums.extend( main.findAll(class_='versenum') )

            # example path --> ./bible_version/KJV/Genesis/1.txt
            with open(os.path.join(CORPUS_PATH, version, book_name, str(chapter)+'.txt'), 'w', encoding='utf8') as f:

                for num in verse_nums:
                    # ex. num --> <sup class="versenum">2 </sup>

                    # find the parent of the superscript tag. look thru these tags and only return text
                    # that isn't tags (don't footnotes. etc.)
                    verse = ''.join( [t for t in num.parent if not isinstance(t, element.Tag)] )

                    # write the verse to the file seprate by new lines
                    f.write( verse )
                    f.write('\n')
            
            # update the bar
            pbar.update(i)
            i += 1

    # finish it off
    pbar.finish()