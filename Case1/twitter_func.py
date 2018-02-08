import twitter
import json
import io

def oauth_login():
    # Access to Twitter API

    CONSUMER_KEY = 'Rs8Ba8b7AOL7IDVIHljuVBERC'
    CONSUMER_SECRET ='84xMvqAD4dfndq29a4RzarCUufdJ9hBHZKcLctqayJXRH6LbLA'
    OAUTH_TOKEN = '389922744-Km3NZ6rShZqSHZ3ZPh24lLBSVxGVqybX8r5B57f8'
    OAUTH_TOKEN_SECRET = 'lJDLpjjyx9QwcCffCJZr4dYKo7aqNwdO7skbjeHxJWZLs'

    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)

    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api

def twitter_trends(twitter_api, woe_id):
    # Discovering the trending topics

    return twitter_api.trends.place(_id=woe_id)

def twitter_search(twitter_api, q, max_results=200, **kw):
    # Searching for tweets

    search_results = twitter_api.search.tweets(q=q, count=100, **kw)

    statuses = search_results['statuses']

    max_results = min(1000, max_results)

    for _ in range(10): # 10*100 = 1000
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError, e: # No more results when next_results doesn't exist
            break

        kwargs = dict([ kv.split('=')
                        for kv in next_results[1:].split("&") ])

        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']

        if len(statuses) > max_results:
            break

    return statuses

def save_json(filename, data):
    with io.open('superbowl.json'.format(filename),
                 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(data, ensure_ascii=False)))

def load_json(filename):
    with io.open('superbowl.json'.format(filename),
                 encoding='utf-8') as f:
        return f.read()

def extract_tweet_entities(statuses):

    #Extracting tweet entities

    if len(statuses) == 0:
        return [], [], [], [], []

    screen_names = [ user_mention['screen_name']
                         for status in statuses
                            for user_mention in status['entities']['user_mentions'] ]

    hashtags = [ hashtag['text']
                     for status in statuses
                        for hashtag in status['entities']['hashtags'] ]

    urls = [ url['expanded_url']
                     for status in statuses
                        for url in status['entities']['urls'] ]

    symbols = [ symbol['text']
                   for status in statuses
                       for symbol in status['entities']['symbols'] ]

    # In some circumstances (such as search results), the media entity
    # may not appear
    if status['entities'].has_key('media'):
        media = [ media['url']
                         for status in statuses
                            for media in status['entities']['media'] ]
    else:
        media = []

    return screen_names, hashtags, urls, media, symbols

def find_popular_tweets(twitter_api, statuses, retweet_threshold=3):

    # finding most popular tweets in a collection of tweets

    return [ status
                for status in statuses
                    if status['retweet_count'] > retweet_threshold ]

from collections import Counter

def get_common_tweet_entities(statuses, entity_threshold=3):

    # Create a flat list of all tweet entities
    tweet_entities = [  e
                        for status in statuses
                            for entity_type in extract_tweet_entities([status])
                                for e in entity_type
                     ]

    c = Counter(tweet_entities).most_common()

    # Compute frequencies
    return [ (k,v)
             for (k,v) in c
                 if v >= entity_threshold
           ]
