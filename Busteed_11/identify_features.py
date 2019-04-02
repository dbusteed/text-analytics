import progressbar as pb # pip install progressbar2
import json
import re

CORPUS_PATH = '../ignore/yelp_AZ_2018.json'
DATA_FILE = 'data.csv'
NUMBER_OF_REVIEWS = 119376

PBAR_DISPLAY = [pb.Percentage(), ' ', pb.Bar(marker='*', left='[', right=']'), ' ', pb.Timer()]

feature_1 = 'exclamation_marks'
feature_2 = 'total_length'

def main():
    with open(DATA_FILE, 'w') as csv:
        csv.write(f'stars,{feature_1},{feature_2}\n')
    
    i = 0
    pbar = pb.ProgressBar(widgets=PBAR_DISPLAY, max_value=NUMBER_OF_REVIEWS, iterator=i)
    pbar.start()

    with open(CORPUS_PATH, 'r', encoding='utf8') as f:
        for line in f:
        
            rev = json.loads(line)
            
            # feature_1
            feat_1_count = len(re.findall(r'!', rev['text']))

            # feature_2
            feat_2_count = len(rev['text'])

            with open(DATA_FILE, 'a') as csv:
                csv.write(f'{rev["stars"]},{feat_1_count},{feat_2_count}\n')

            pbar.update(i)
            i += 1

        pbar.finish()

if __name__ == '__main__':
    main()