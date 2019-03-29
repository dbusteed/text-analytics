"""
Davis Busteed
LING 360
Homework #10

This program uses the LDA (Latent Dirichlet Allocation) algorithm, 
available in the gensim Python module, to discover topics in the 
news articles.
"""

# import modules
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

import pyLDAvis.gensim
import pyLDAvis
import gensim

from pandas import DataFrame
import string
import os
import re

# default values / script parameters
CORPUS_PATH = '..\\ignore\\news_universe'
NUM_TOPICS = 4
NUM_WORDS = 10

# wordlists / model objects
stop = set(stopwords.words('english'))
exclude = set(string.punctuation) 
lemma = WordNetLemmatizer()
lda = gensim.models.ldamodel.LdaModel

# this function takes a file path, reads and returns the contents
def get_file_text(path):
    return open(os.path.join(CORPUS_PATH, path), encoding='utf8').read()

# this function takes a bunch of text (doc)
# and removes stopwords, puncation, then lemmatizes it
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

# main function
def main():
    # get all the '.txt' file from the specified directory
    files = [f for f in os.listdir(CORPUS_PATH) if re.search(r'\.txt', f)]

    # grab all the text from the text files
    raw_text = [get_file_text(f) for f in files]

    # clean the raw_text
    clean_text = [clean(doc).split() for doc in raw_text]

    # create a term dictionary, where every unique term is assigned an index. 
    term_dict = gensim.corpora.Dictionary(clean_text)

    # converting list of documents into Document Term Matrix 
    doc_term_matrix = [term_dict.doc2bow(doc) for doc in clean_text]

    # creating the object for LDA model using gensim library
    lda_model = lda(doc_term_matrix, num_topics=NUM_TOPICS, id2word=term_dict, passes=50)

    # grab the topics from our lda_model
    topics = lda_model.print_topics(num_topics=NUM_TOPICS, num_words=NUM_WORDS)

    # dictionary for holding topics and keywords
    results = {}

    # grab the keywords for each topic, and save them to the dictionary
    for i,topic in enumerate(topics):    
        results['topic_'+str(i+1)] = re.findall(r'"(.*?)"', str(topic))

    # convert to DataFrame object and write to CSV
    DataFrame.from_dict(results).to_csv('results.csv', index=False)

    # create a topic map and show it (should spin up local server and display in browser)
    topic_map = pyLDAvis.gensim.prepare(lda_model, doc_term_matrix, term_dict)
    pyLDAvis.show(topic_map)
        
if __name__ == '__main__':
    main()