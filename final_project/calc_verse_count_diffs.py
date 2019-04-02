from project_settings import CORPUS_PATH, CHAPTERS_IN_BIBLE
from project_settings import list_dir_by_time
from my_progressbar import start_pbar
import os

counts = {}

for version in os.listdir(CORPUS_PATH):

    pbar, i = start_pbar(CHAPTERS_IN_BIBLE, f'Counting # of verses for each chapter in {version} Bible')

    counts[version] = {}

    # get all the books for this version
    books = list_dir_by_time( os.path.join(CORPUS_PATH, version) )

    for book_path in books:

        book_name = os.path.split(book_path)[1]
        counts[version][ book_name ] = []

        chapters = list_dir_by_time( book_path )

        for c,chap in enumerate(chapters):

            chap_verse = [(c+1),0]

            txt = open(chap, 'r', encoding='utf8', errors='ignore').read()

            for verse in txt.split('\n'):

                chap_verse[1] += 1
            
            counts[version][ book_name ].append(chap_verse)

            pbar.update(i)
            i += 1

    pbar.finish()


# Resutling map will look like this:
# { 
#     'KJV': {'Genesis': [[1, 32], [2, 26] ...'},
#     'ESV': {'Genesis': [[1, 32], [2, 26] ...'},
#     ...
# }
    
ver = list(counts)

out_string = ''

# this loop will make the indexes to compare each version
# to every other version once
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
            
print(f'\nSummary of verse counts written to \'diff_summary.txt\'\n')

with open( os.path.join('other_data', 'diff_summary.txt'), 'w', encoding='utf8') as f:
    f.write(out_string)