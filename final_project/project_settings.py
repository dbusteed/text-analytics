import os

CORPUS_PATH = 'bible_versions'
CHAPTERS_IN_BIBLE = 1189
VERSION_LIST = ['KJV', 'ESV', 'NASB', 'NLT', 'NIV', 'NKJV']

def list_dir_by_time(path):
    items = os.listdir(path)
    items = [os.path.join(path,i) for i in items]
    items.sort(key=lambda x: os.path.getmtime(x))
    return items