# Davis Busteed -- LING 360 -- HW #9

# Instructions:
# Write a Python program that web scrapes in order to create a small corpus of texts from the internet. Your program should 
# start at a webpage that is hard-coded into your .py file. The program should randomly choose ten links on the starting 
# webpage and then visit those other webpages. If there are fewer than ten, all the links available should be used. At each 
# webpage, the program should web scrape the text and save it to a .txt file on your computer's hard drive. The program 
# should perform any additional cleaning needed, for example, to exclude javascript function definitions. Each file should 
# have a distinct name so that, when finished, the program will have written ten .txt files with the text of the ten 
# websites your program visited.

# import modules
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import random
import re
import os

# directory for our 'corpus' files to go
CORPUS_PATH = 'webpages'

# create the folder if it doesn't exist already
# note: the above corpus_path should be a directory within 
# this working directory (same level as this script), not 
# something like '../stuff' or './stuff/other/'
if not os.path.exists(CORPUS_PATH):
    os.mkdir(CORPUS_PATH)

# this function will grab a webpage from the url, take the text from 
# all the <p> tags and save them to a txt file,
# and return all the external links (unless specified otherwise)
def process_page(url, return_links=True):

    # get html and parse to BeautifulSoup object
    page = requests.get(url).text
    ppage = BeautifulSoup(page, 'html.parser') # 'ppage' --> 'processed page'

    # scrape text for <p> tags
    paragraphs = ppage.findAll('p')

    # get the webpage_name for logging
    webpage_name = urlparse(url).netloc

    # create a file_name from the url. get rid of illegal characters for file naming.
    # we can't use webpage_name for the filename cause it won't be unique
    # for example wikipedia.org/thing would overwrite wikipedia.org/other if they 
    # both were named as wikipedia.org.txt
    file_name = re.sub(r'(https?)|[/\\*\?":<>\|]', '', url)

    # open the file
    with open(os.path.join(CORPUS_PATH, file_name+'.txt'), 'w', encoding='utf8') as f:

        # log to console
        print(f'processing page: {webpage_name}')

        # .txt header
        f.write(url + '\n\n')
        
        # if no <p> tags were found write out the following
        if len(paragraphs) == 0:
            f.write('no <p> tags found')

        # write out each <p> tags contents
        else:
            for p in paragraphs:
                p = re.sub(r'<script>.*</script>', '', p.get_text()) # remove any javascript
                f.write(p + '\n')

    # since this defaults to true, this block will
    # not run only if specifically told not to gather/return links 
    if return_links:

        # only get external links (ones that start with http)
        links = [a.get('href') for a in ppage.findAll('a', href={re.compile(r'^http')})]

        # keep only unique links
        return list( set(links) )

# define a starting url and get the links 
# (i chose a search engine since it would have more variation in external links)
urls = 'https://www.bing.com/search?q=cabbage'
links = process_page(urls)

# randomize the order of links so we can test different results
random.shuffle(links)

# number of pages to process
pages_to_scrape = 10

# if the page didn't return enough links, then
# just go process all the available links
if len(links) < pages_to_scrape:
    pages_to_scrape = len(links)

# loop thru and process each page
for i in range(pages_to_scrape):
    process_page( links[i], return_links=False )