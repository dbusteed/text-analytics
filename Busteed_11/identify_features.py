# Davis Busteed -- LING 360 -- HW #11

# This script identifies linguistic features that may be 
# correlated with the number of stars a business receives
# on online reviews

# import modules
from statistics import mean
import progressbar as pb # pip install progressbar2
import json
import re

# define constants
CORPUS_PATH = '../ignore/yelp_AZ_2018.json'
DATA_FILE = 'data.csv'
NUMBER_OF_REVIEWS = 119376

# these are the feature labels!
FEATS = ['exclamation_marks', 'avg_sent_length', 'upper_case_words', 'total_length']

# this is for the progress bar
PBAR_DISPLAY = [pb.Percentage(), ' ', pb.Bar(marker='*', left='[', right=']'), ' ', pb.Timer()]

# main function (allows for importing constants)
def main():

    # first write the header for CSV
    with open(DATA_FILE, 'w') as out_csv:
        out_csv.write(f'stars,{",".join(FEATS)}\n')
    
    # set up and start the progress bar
    i = 0
    pbar = pb.ProgressBar(widgets=PBAR_DISPLAY, max_value=NUMBER_OF_REVIEWS, iterator=i)
    pbar.start()

    # open the JSON and CSV file
    with open(CORPUS_PATH, 'r', encoding='utf8') as review_file, open(DATA_FILE, 'a') as out_csv:

            # go thru each line in the review_file
            for line in review_file:
            
                # load up the review (now it's a 'dict' object)
                rev = json.loads(line)

                feat_counts = []   

                # count feature_1 (as defined above)
                feat_counts.append( len(re.findall(r'!', rev['text'])) )

                # count feature_2
                sents = re.split(r'[\.!\?]', rev['text'])
                feat_counts.append( mean([len(s) for s in sents]) )

                # count feature_3
                feat_counts.append( len(re.findall(r'\b([A-Z]){2,}\b', rev['text'])) )

                # count feature_4
                feat_counts.append( len(rev['text']) )

                # write the stars and features counts to the 
                # CSV file (notice method='a' for appending)
                out_csv.write(f'{rev["stars"]},{",".join(str(fc) for fc in feat_counts)} \n')

                # update the progress bar
                pbar.update(i)
                i += 1

            # end the progress bar
            pbar.finish()

# only run the main function when being directly called
# (don't run this stuff when values being imported in)
if __name__ == '__main__':
    main()