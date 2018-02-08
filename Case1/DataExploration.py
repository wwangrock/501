import json
import io
from collections import Counter
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import twitter
import tweepy

auth = tweepy.OAuthHandler('Rs8Ba8b7AOL7IDVIHljuVBERC', '84xMvqAD4dfndq29a4RzarCUufdJ9hBHZKcLctqayJXRH6LbLA')
auth.set_access_token('389922744-Km3NZ6rShZqSHZ3ZPh24lLBSVxGVqybX8r5B57f8', 'lJDLpjjyx9QwcCffCJZr4dYKo7aqNwdO7skbjeHxJWZLs')

api = tweepy.API(auth)

public_tweets = api.home_timeline()

#from DataCollection import *
#from DataCollection import *
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

with io.open('superbowl.json',encoding='utf-8') as f:
    statuses = json.load(f)

status_texts = [ status['text']
                 for status in statuses ]

screen_names = [ user_mention['screen_name']
                 for status in statuses
                     for user_mention in status['entities']['user_mentions'] ]

user_mentions = [ user_mention['id']
                  for status in statuses
                      for user_mention in status['entities']['user_mentions']]

hashtags = [ hashtag['text']
             for status in statuses
                 for hashtag in status['entities']['hashtags'] ]

# Compute a collection of all words from all tweets
words = [ w
          for t in status_texts
              for w in t.split() ]

counts = Counter(words)
###################################



import sys
import time
from urllib2 import URLError
from httplib import BadStatusLine
import json
import twitter
from functools import partial
from sys import maxint

def make_twitter_request(twitter_api_func, max_errors=10, *args, **kw):

    # A nested helper function that handles common HTTPErrors. Return an updated
    # value for wait_period if the problem is a 500 level error. Block until the
    # rate limit is reset if it's a rate limiting issue (429 error). Returns None
    # for 401 and 404 errors, which requires special handling by the caller.
    def handle_twitter_http_error(e, wait_period=2, sleep_when_rate_limited=True):

        if wait_period > 3600: # Seconds
            print >> sys.stderr, 'Too many retries. Quitting.'
            raise e

        # See https://dev.twitter.com/docs/error-codes-responses for common codes

        if e.e.code == 401:
            print >> sys.stderr, 'Encountered 401 Error (Not Authorized)'
            return None
        elif e.e.code == 404:
            print >> sys.stderr, 'Encountered 404 Error (Not Found)'
            return None
        elif e.e.code == 429:
            print >> sys.stderr, 'Encountered 429 Error (Rate Limit Exceeded)'
            if sleep_when_rate_limited:
                print >> sys.stderr, "Retrying in 15 minutes...ZzZ..."
                sys.stderr.flush()
                time.sleep(60*15 + 5)
                print >> sys.stderr, '...ZzZ...Awake now and trying again.'
                return 2
            else:
                raise e # Caller must handle the rate limiting issue
        elif e.e.code in (500, 502, 503, 504):
            print >> sys.stderr, 'Encountered %i Error. Retrying in %i seconds' % \
                (e.e.code, wait_period)
            time.sleep(wait_period)
            wait_period *= 1.5
            return wait_period
        else:
            raise e

    # End of nested helper function

    wait_period = 2
    error_count = 0

    while True:
        try:
            return twitter_api_func(*args, **kw)
        except twitter.api.TwitterHTTPError, e:
            error_count = 0
            wait_period = handle_twitter_http_error(e, wait_period)
            if wait_period is None:
                return
        except URLError, e:
            error_count += 1
            time.sleep(wait_period)
            wait_period *= 1.5
            print >> sys.stderr, "URLError encountered. Continuing."
            if error_count > max_errors:
                print >> sys.stderr, "Too many consecutive errors...bailing out."
                raise
        except BadStatusLine, e:
            error_count += 1
            time.sleep(wait_period)
            wait_period *= 1.5
            print >> sys.stderr, "BadStatusLine encountered. Continuing."
            if error_count > max_errors:
                print >> sys.stderr, "Too many consecutive errors...bailing out."
                raise


def get_friends_followers_ids(twitter_api, screen_name=None, user_id=None,
                              friends_limit=maxint, followers_limit=maxint):

    # Must have either screen_name or user_id (logical xor)
    assert (screen_name != None) != (user_id != None), \
    "Must have screen_name or user_id, but not both"

    # See https://dev.twitter.com/docs/api/1.1/get/friends/ids and
    # https://dev.twitter.com/docs/api/1.1/get/followers/ids for details
    # on API parameters

    get_friends_ids = partial(make_twitter_request, twitter_api.friends.ids,
                              count=5000)
    get_followers_ids = partial(make_twitter_request, twitter_api.followers.ids,
                                count=5000)

    friends_ids, followers_ids = [], []

    for twitter_api_func, limit, ids, label in [
                    [get_friends_ids, friends_limit, friends_ids, "friends"],
                    [get_followers_ids, followers_limit, followers_ids, "followers"]
                ]:

        if limit == 0: continue

        cursor = -1
        while cursor != 0:

            # Use make_twitter_request via the partially bound callable...
            if screen_name:
                response = twitter_api_func(screen_name=screen_name, cursor=cursor)
            else: # user_id
                response = twitter_api_func(user_id=user_id, cursor=cursor)

            if response is not None:
                ids += response['ids']
                cursor = response['next_cursor']

            print >> sys.stderr, 'Fetched {0} total {1} ids for {2}'.format(len(ids),
                                                    label, (user_id or screen_name))

            # XXX: You may want to store data during each iteration to provide an
            # an additional layer of protection from exceptional circumstances

            if len(ids) >= limit or response is None:
                break

    # Do something useful with the IDs, like store them to disk...
    return friends_ids[:friends_limit], followers_ids[:followers_limit]

# Sample usage

twitter_api = oauth_login()

friends_ids, followers_ids = get_friends_followers_ids(twitter_api,
                                                       screen_name="Patriots",
                                                       friends_limit=20,
                                                       followers_limit=20)

#print friends_ids
#print followers_ids

#ids = [status['user']['id']
        #for status in statuses]
friends_names = []
for i in friends_ids:
    u = api.get_user(i)
    friends_names.append(u.screen_name)
followers_names = []
for i in followers_ids:
    u = api.get_user(i)
    followers_names.append(u.screen_name)
#print friends_names
#print followers_names

x = PrettyTable(['friends_id','friends_name'])
x.align['friends_id'] = 'l'
x.align['friends_name'] = 'l'
x.padding_width = 1
for i in range(len(friends_ids)):
    x.add_row([friends_ids[i],friends_names[i]])

y = PrettyTable(['followers_id','followers_name'])
y.align['followers_id'] = 'l'
y.align['followers_name'] = 'l'
y.padding_width = 1
for i in range(len(followers_ids)):
    y.add_row([followers_ids[i],followers_names[i]])

print (x)
print (y)
