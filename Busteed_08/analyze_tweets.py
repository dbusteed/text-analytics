import re
import json
import statistics as st
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from get_tweets import MAIN_HASHTAG

SUBTOPIC = 'galaxy'
STOPWORDS = stopwords.words('english')

def process_tweet(key, text):

    # add the sentiment compound score
    res[key]['sent_scores'].append( sia.polarity_scores(text)['compound'] )

    # put pos/neg tweets about the product (subtopic) into the lists
    if key == 'sub':
        if sia.polarity_scores(text)['compound'] > 0:
            res[key]['pos_tweets'] += text + ' '
        else:
            res[key]['neg_tweets'] += text + ' '


sia = SentimentIntensityAnalyzer()

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

# loop thru the JSON strings 
with open(f'{MAIN_HASHTAG}_tweets.json', 'r', encoding='utf8') as f:
    for raw_tweet in f:

        # convert the string into a dict, then grab the full_text of that tweet
        text = json.loads(raw_tweet)['full_text']

        # if the subtopic (specific product of a company) is in the tweet
        if SUBTOPIC in text.lower():
            process_tweet('sub', text)

        # process all the tweets that had the main hashtag (all strings in the JSON)
        process_tweet('main', text)

for sent in ['pos', 'neg']:
    s = res['sub'][f'{sent}_tweets'].lower()
    
    s = re.sub(r'(https?[^\s]*)|(#\w+)|(@\w+)|(rt)', '', s)
    s = re.sub(rf'{MAIN_HASHTAG}|{SUBTOPIC}', '', s)
    
    tokens = re.split(r'[&#%\d:"\]\[\u201c\u201d\s+\.\?!,)(/-]', s)
    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 1]

    for word in tokens:
        if word not in res['sub'][f'{sent}_most']:
            res['sub'][f'{sent}_most'][word] = 1
        else:
            res['sub'][f'{sent}_most'][word] += 1

    res['sub'][f'{sent}_most'] = sorted(res['sub'][f'{sent}_most'].items(), key=lambda x:x[1], reverse=True)[:5]

# output the results
print('\nSentiment comparisons')
for k in res.keys():
    res[k]['total_sent'] = st.mean( res[k]['sent_scores'] )
    print(f'Compound sentiment for {res[k]["hash"]}: {res[k]["total_sent"]:05.3f}')

# 
for sent in ['pos', 'neg']:
    print(f'\nTop 5 words in {sent}-ative tweets')
    for (w, _) in res['sub'][f'{sent}_most']:
        print(w)

print()