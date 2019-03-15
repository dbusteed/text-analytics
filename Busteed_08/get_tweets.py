# Davis Busteed -- LING 360 -- HW 8

# import modules
import api_config  # api_config.py located in working directory,
import tweepy      # add your own api_config or hardcode tokens to run script
import json

MAIN_HASHTAG = 'samsung'
TWEET_COUNT = 1000

def main():
    
    consumer_key = api_config.consumer_key
    consumer_secret_key = api_config.consumer_secret_key
    # consumer_key = YOUR_KEY_HERE
    # consumer_secret_key = YOUR_KEY_HERE

    access_token = api_config.access_token
    access_token_secret = api_config.access_token_secret
    # access_token = YOUR_KEY_HERE
    # access_token_secret = YOUR_KEY_HERE

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    tweets = tweepy.Cursor(api.search, q=f'#{MAIN_HASHTAG}', tweet_mode='extended', lang='en').items(TWEET_COUNT)

    # save our tweets!
    with open(f'{MAIN_HASHTAG}_tweets.json', 'w', encoding='utf8') as f:
        for t in tweets:
            f.write(json.dumps(t._json, ensure_ascii=True))
            f.write('\n')

if __name__ == '__main__':
    main()