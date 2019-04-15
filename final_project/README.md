# Final Project for LING 360

### Set of Python scripts that explores the differences among the various translations of the Bible, in an attempt to find which translation is most similar to the King James Version (KJV)

#### Virtualenv Setup (optional)
These scripts use a lot of common libraries, but if you wanna play it safe, you can use a virtual environment and install the necessary modules

```
(venv) C:\text-analytics\final_project> pip install -r requirements.txt
```

#### Explaination (and suggested running order) of scripts

1. Corpus creation
    1. `bible_scraper.py`
        * Scrapes Biblegateway.com for the text of different Bible translations
        * Creates and populates a corpus, .TXT file for each chapter of each book of each version
        * This takes ~1 hour
    2. `create_chapter_index.py`
        * Creates `chapter_index.csv` used in other scripts to match book/chapter names chapter lists
        * CSV files like this are stored in `misc_data/`

2. Calculate sentiment scores
    1. `calc_chap_sentiments.py`
        * Creates `chapter_sentiments.csv` with chapter sentiments
    2. `visualize_sentiment.py`
        * Creates visualizations of sentiment differences

2. Calculate Levenshtein (fuzzy) scores
    1. `calc_text_diffs.py`
        * Creates `fuzz_scores.csv` with Levenshtein distance for each chapter compared with every version
    2. `get_kjv_fuzz_scores.py`
        * Creates `kjv_fuzz_scores.csv` and `kjv_fuzz_scores_by_book.csv`, subsections of the `fuzz_scores.csv`
    3. `visualize_fuzz_scores.py`
        * Creates visualizations of textual differences

3. Other
    1. `shared/` 
        * Contains a settings files and snippets used in a lot of the scripts
    2. `calc_verse_count_diffs.py`
        * Calculates the differences between versions solely based on verse count per chapter
        * This isn't the best approach, as a couple of the Bible chapters were written in poetry form, in which acutal verse count couldn't be recorded properly