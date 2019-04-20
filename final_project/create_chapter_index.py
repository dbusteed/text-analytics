# Davis Busteed -- LING 360 -- Final Project

#-------------------------------------------------------------#
#                                                             #
#   OVERVIEW -- this script will creates an 'index' from the  #
#               corpus, than can be combined to CSV output    #
#               files to make analysis easier                 #
#                                                             #
#-------------------------------------------------------------#

# required modules
from shared.project_settings import CORPUS_PATH, CHAPTERS_IN_BIBLE, MISC_PATH
from shared.project_settings import list_dir_by_time
import os

# i is just the overall index of the index.csv
i = 0

# other starting values
out_string = ''
OUT_FILE = 'chapter_index.csv'

# this could be any version, since tests
# have shown all versions have same chapters
version = 'KJV'

# make the path if not exists
if not os.path.exists(MISC_PATH):
    os.mkdir(MISC_PATH)

# open up the index file
with open( os.path.join(MISC_PATH, OUT_FILE), 'w', encoding='utf8') as f:
    f.write('zero_index,one_index,book,chapter,start_of_book\n')

# get all the books (in order of created date)
books = list_dir_by_time( os.path.join(CORPUS_PATH, version) )

# go thru the books
for book_path in books:

    # get the name and number of chapters
    book_name = os.path.split(book_path)[1]
    num_chaps = len(os.listdir(book_path))

    # write this out to the file
    for num in range(1, num_chaps+1):
        out_string += f'{i},{i+1},{book_name},{book_name} {num},{num == 1}\n'
        i += 1

# write the string out
with open( os.path.join(MISC_PATH, OUT_FILE), 'a', encoding='utf8') as f:
    f.write(out_string)

# message for user
print(f'\nIndex file written out to {os.path.join(MISC_PATH, OUT_FILE)}\n')