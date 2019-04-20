# Davis Busteed -- LING 360 -- Final Project

#
#   NOTE: this script isn't as useful as it once was. after
#           rewriting the scraper to deal with poetry fomrated
#           chapters, some chapters are just big long strings, 
#           which can't really be understood by this script
#

#--------------------------------------------------------------#
#                                                              #
#   OVERVIEW -- this script will read thru the Bible corpus    # 
#               and checks for differences in book,chapter,    #
#               and verse numbers, then prints out a report    #
#                                                              #
#--------------------------------------------------------------#

# import modules
from shared.project_settings import CORPUS_PATH, CHAPTERS_IN_BIBLE, MISC_PATH
from shared.project_settings import list_dir_by_time
from shared.my_progressbar import start_pbar
import os

OUT_FILE = 'diff_summary.txt'

# counter dictionary (example structure shown below)
counts = {}

#----------------------------------------------------#
#                                                    #
#   STEP 1 -- grab number of chapters and verses     #
#             for each bible version                 #
#                                                    #
#----------------------------------------------------#

for version in os.listdir(CORPUS_PATH):

    pbar, i = start_pbar(CHAPTERS_IN_BIBLE, f'Counting # of verses for each chapter in {version} Bible')

    counts[version] = {}

    # get all the books for this version
    books = list_dir_by_time( os.path.join(CORPUS_PATH, version) )

    # go thru the books
    for book_path in books:

        # manage the dictionary
        book_name = os.path.split(book_path)[1]
        counts[version][ book_name ] = []

        # get chapters
        chapters = list_dir_by_time( book_path )

        # go thru the chatpers
        for c,chap in enumerate(chapters):

            # chap_verse is just the chapter and the verses in that chapter
            chap_verse = [(c+1),0]

            txt = open(chap, 'r', encoding='utf8', errors='ignore').read()

            # verses split on \n
            for verse in txt.split('\n'):

                chap_verse[1] += 1
                
            # put nums in
            counts[version][ book_name ].append(chap_verse)

            # prog bar
            pbar.update(i)
            i += 1

    pbar.finish()


# Resutling dictionary will look like this:
# { 
#     'KJV': {'Genesis': [[1, 50], [2, 26] ...'},
#     'ESV': {'Genesis': [[1, 50], [2, 26] ...'},
#     ...
# }


#------------------------------------------------------#
#                                                      #
#   STEP 2 -- check every version with every version   #
#             and check that they have same number     #
#             of book, chapters, and verses. write     #
#             results out to a .txt file               #
#                                                      #
#------------------------------------------------------#
    
ver = list(counts)
out_string = ''

# this loop will make the indexes to compare each version
# to every other version once (ex: 0-1, 0-2, 1-2)
for j in range(0, len(ver)):
    for k in range(j+1, len(ver)):

        total_diffs = 0

        # header
        out_string += f'{ver[j]} and {ver[k]}\n------------\n'

        # check number of books
        if list(counts[ver[j]]) == list(counts[ver[k]]):
            out_string += 'SAME number and order of books\n'
        else:
            out_string += 'DIFFERENT number and order of books\n'

        # check number of chapters
        out_string += f'SAME number of chapters in every book unless otherwise stated.\n'
        out_string += f'SAME number of verses in every chapter unless otherwise stated.\n'
        for book in counts[ver[j]]:
            if len(counts[ver[j]][book]) != len(counts[ver[k]][book]):
                out_string += f'DIFFERENT number of chapters in {book}\n'
                out_string += f'>>> {ver[j]}: {len(counts[ver[j]][book])} chapters -- {ver[k]}: {len(counts[ver[k]][book])} chapters'

            # check same number of verses
            for idx in range(0, len(counts[ver[j]][book])):
                if counts[ver[j]][book][idx] != counts[ver[k]][book][idx]:
                    out_string += f'{book} {counts[ver[j]][book][idx][0]}: '
                    out_string += f'{ver[j]}-{counts[ver[j]][book][idx][1]} verses, '
                    out_string += f'{ver[k]}-{counts[ver[k]][book][idx][1]} verses\n'
                    
                    total_diffs += abs(counts[ver[j]][book][idx][1] - counts[ver[k]][book][idx][1])

        out_string += f'# of different verse counts: {total_diffs}\n\n'
            
with open( os.path.join(MISC_PATH, OUT_FILE), 'w', encoding='utf8') as f:
    f.write(out_string)

print(f'\nSummary of verse counts written to {os.path.join(MISC_PATH, OUT_FILE)}\n')