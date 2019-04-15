from shared.project_settings import CORPUS_PATH, CHAPTERS_IN_BIBLE, MISC_PATH
from shared.project_settings import list_dir_by_time
import os

i = 0
out_string = ''
OUT_FILE = 'chapter_index.csv'

# this could be any version, since tests
# have shown all versions have same chapters
version = 'KJV'

if not os.path.exists(MISC_PATH):
    os.mkdir(MISC_PATH)

with open( os.path.join(MISC_PATH, OUT_FILE), 'w', encoding='utf8') as f:
    f.write('zero_index,one_index,book,chapter,start_of_book\n')

books = list_dir_by_time( os.path.join(CORPUS_PATH, version) )

for book_path in books:

    book_name = os.path.split(book_path)[1]
    num_chaps = len(os.listdir(book_path))

    for num in range(1, num_chaps+1):
        out_string += f'{i},{i+1},{book_name},{book_name} {num},{num == 1}\n'
        i += 1

with open( os.path.join(MISC_PATH, OUT_FILE), 'a', encoding='utf8') as f:
    f.write(out_string)

print(f'\nIndex file written out to {os.path.join(MISC_PATH, OUT_FILE)}\n')