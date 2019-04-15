# Davis Busteed -- LING 360 -- Final Project

#---------------------------------------------------------------#
#                                                               #
#   This file cotains values and functions that are shared      #
#   throughout many different scipts, they can be imported      #
#   in to that script with 'from shared.project_settings import X'     #
#                                                               #
#---------------------------------------------------------------#

import os

CORPUS_PATH = 'bible_versions'
MISC_PATH = 'misc_data'
CHAPTERS_IN_BIBLE = 1189
VERSION_LIST = ['KJV', 'ESV', 'NASB', 'NLT', 'NIV', 'NKJV']

# TODO
def list_dir_by_time(path):
    items = os.listdir(path)
    items = [os.path.join(path,i) for i in items]
    items.sort(key=lambda x: os.path.getmtime(x))
    return items