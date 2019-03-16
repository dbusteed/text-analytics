# Davis Busteed -- LING 360 -- HW 8

# import modules
import re
import json
import statistics as st
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from get_tweets import MAIN_HASHTAG # get_tweets.py located in same directory

# define constants
SUBTOPIC = 'galaxy'
STOPWORDS = stopwords.words('english')

# function for processing the tweets
def process_tweet(key, text):

    # add the sentiment compound score
    res[key]['sent_scores'].append( sia.polarity_scores(text)['compound'] )

    # put pos/neg tweets about the product (subtopic) into the lists
    if key == 'sub':
        if sia.polarity_scores(text)['compound'] > 0:
            res[key]['pos_tweets'] += text + ' '
        else:
            res[key]['neg_tweets'] += text + ' '

# define the Sentiment analyzer object
sia = SentimentIntensityAnalyzer()

# dictionary for keeping track ofc counts / sentiments
# 'main' refers to the main hashtag (the company)
# 'sub' refers to the subtopic (a product of the company)
res = {
    'main': { 
        'hash': MAIN_HASHTAG, 
        'sent_scores': [],
    },
    'sub': { 
        'hash': SUBTOPIC, 
        'sent_scores': [], 
        'pos_tweets': '', 
        'neg_tweets': '',
        'pos_most': {},
        'neg_most': {}, 
    },
}

# loop thru the JSON strings and process tweets
with open(f'{MAIN_HASHTAG}_tweets.json', 'r', encoding='utf8') as f:
    for raw_tweet in f:

        # convert the string into a dict, then grab the full_text of that tweet
        text = json.loads(raw_tweet)['full_text']

        # if the subtopic (specific product of a company) is in the tweet
        if SUBTOPIC in text.lower():
            process_tweet('sub', text)

        # process all the tweets that had the main hashtag (all strings in the JSON)
        process_tweet('main', text)

# find top 5 words for both pos_tweets and neg_tweets
for sent in ['pos', 'neg']:

    # grab the tweets, 's' --> one big string tweets
    # (see process_tweet function)
    s = res['sub'][f'{sent}_tweets'].lower()
    
    # get rid of links, #hashtags, @usernames, and 'RT' indicators
    # also remove instances of the company hashtag and product
    # I'm aware the next two line can be combinded into one, but this is more readable
    s = re.sub(r'(https?[^\s]*)|(#\w+)|(@\w+)|(rt)', '', s)
    s = re.sub(rf'{MAIN_HASHTAG}|{SUBTOPIC}', '', s)
    
    # split the string of tweets into words on punctuation marks, symbols, and quotes
    tokens = re.split(r'[&#%\d:"\]\[\u201c\u201d\s+\.\?!,)(/-]', s)

    # remove all tokesn that are in the STOPWORDS or are 1 char (also gets rid of '')
    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 1]

    # loop thru each token
    for word in tokens:

        # count each instance of a word
        if word not in res['sub'][f'{sent}_most']:
            res['sub'][f'{sent}_most'][word] = 1
        else:
            res['sub'][f'{sent}_most'][word] += 1

    # replace the word freq dictionary with a sorted list of tuples (only top 5 tho, notice the [:5])
    res['sub'][f'{sent}_most'] = sorted(res['sub'][f'{sent}_most'].items(), key=lambda x:x[1], reverse=True)[:5]

# output time!
print('\nSentiment comparisons\n-------------')
for k in res.keys():

    # calculate the average sentiment and output 
    res[k]['total_sent'] = st.mean( res[k]['sent_scores'] )
    print(f'Compound sentiment for "{res[k]["hash"]}": {res[k]["total_sent"]:05.3f}')

# dipsplay which was greater
if res['main']['total_sent'] > res['sub']['total_sent']:
    print(f'\nSentiment for "{res["main"]["hash"]}" (the company) is greater than "{res["sub"]["hash"]}" ' )
else:
    print(f'\nSentiment for "{res["sub"]["hash"]}" (the product) is greater than "{res["main"]["hash"]}" ' )

# show the top 5 words for positive and negative tweets
for sent in ['pos', 'neg']:
    print(f'\nTop 5 words for {sent} tweets\n-------------')
    for (w, _) in res['sub'][f'{sent}_most']:
        print(w)

print()