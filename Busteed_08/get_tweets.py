# Davis Busteed -- LING 360 -- HW 8

# import modules
import api_config  # api_config.py located in working directory,
import tweepy      # add your keys to api_config or hardcode tokens to run script
import json        # if hardcoding the keys, then remove 'import api_config'

# the main hashtag / topic to look for
MAIN_HASHTAG = 'samsung'
TWEET_COUNT = 1000

# main() / if __name__ stuff at the bottom allows me to 
# import the MAIN_HASHTAG constant from above into the 
# other scripts, without running the code below
def main():
    
    # add your keys here!
    consumer_key = api_config.consumer_key
    consumer_secret_key = api_config.consumer_secret_key

    access_token = api_config.access_token
    access_token_secret = api_config.access_token_secret

    # authenticate thru Twitter with the keys
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)

    # connect to the API
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # go get the tweets! get 280 char english tweets with our hashtag of choice
    tweets = tweepy.Cursor(api.search, q=f'#{MAIN_HASHTAG}', tweet_mode='extended', lang='en').items(TWEET_COUNT)

    # save our tweets! note: this isn't a 'real' json file, so after
    # creating it, your IDE may show errors. it is purposefully formatted
    # as a file of JSON strings
    with open(f'{MAIN_HASHTAG}_tweets.json', 'w', encoding='utf8') as f:
        for t in tweets:
            f.write(json.dumps(t._json, ensure_ascii=True))
            f.write('\n')

# this is explained above
if __name__ == '__main__':
    main()