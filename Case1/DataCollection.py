
import twitter
import json
import io
from urllib import unquote

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
twitter_api = oauth_login()

# Store the tweets into a local file
q = '#SuperBowl'
count = 100

search_results = twitter_api.search.tweets(q=q, count=count)
statuses = search_results['statuses']

for _ in range(29):
    print "Length of statuses", len(statuses)
    try:
        next_results = search_results['search_metadata']['next_results']
    except KeyError, e:
        break

    kwargs = dict([ kv.split('=') for kv in unquote(next_results[1:]).split("&") ])

    search_results = twitter_api.search.tweets(**kwargs)
    statuses += search_results['statuses']

with io.open('superbowl.json','w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(statuses, ensure_ascii=False)))
