from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint
import asyncio


async def main():
    MINIMUM_TWEETS = 50
    QUERY = 'coding'

    async def get_tweets(tweets):
        if tweets is None:
            print('Getting Tweets...')
            tweets = await client.search_tweet(QUERY, product='Top')
        else:
            wait_time = randint(7, 15)
            print(f'Getting more Tweets, waiting {wait_time} seconds...')
            time.sleep(wait_time)
            tweets = await tweets.next()
        return tweets

    config = ConfigParser()
    config.read('config.ini')
    username = config['X']['username']
    password = config['X']['password']
    email = config['X']['email']

    # csv file to store the tweets
    with open('output.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['No.', 'Name', 'Text', 'Full Text', 'Created At', 'Retweets', 'Likes'])

    client = Client(language='en-US')

    # Login and retrieve cookie
    # await client.login(auth_info_1=username, auth_info_2=email, password=password)
    # client.save_cookies('cookies.json')

    # alternatively, load a saved cookie
    client.load_cookies('cookies.json')

    # get tweets
    tweet_count = 0
    tweets = None

    while tweet_count < MINIMUM_TWEETS:
        try:
            tweets = await get_tweets(tweets)
        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            print(f'Rate limit reached. Waiting until {rate_limit_reset}')
            wait_time = rate_limit_reset - datetime.now()
            time.sleep(wait_time.total_seconds())
            continue

        if not tweets:
            print('NO MORE TWEETS FOUND')
            break

        for tweet in tweets:
            tweet_count += 1
            tweet_data = [tweet_count, tweet.user.name, tweet.text, tweet.full_text, tweet.created_at,
                          tweet.retweet_cout, tweet.favorite_count]
            # print(tweet_data)
            with open('output.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(tweet_data)
            # print(vars(tweet))

        print(f' Got {tweet_count} tweets')


if __name__ == '__main__':
    asyncio.run(main())
