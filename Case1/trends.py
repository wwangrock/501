
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

# The Yahoo! Where On Earth ID for the entire world is 1.
# See https://dev.twitter.com/docs/api/1.1/get/trends/place and
# http://developer.yahoo.com/geo/geoplanet/

WORLD_WOE_ID = 1
US_WOE_ID = 23424977

# Prefix ID with the underscore for query string parameterization.
# Without the underscore, the twitter package appends the ID value
# to the URL itself as a special case keyword argument.

world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)
us_trends = twitter_api.trends.place(_id=US_WOE_ID)

#print world_trends
#print
#print us_trends

import json


print json.dumps(us_trends, indent=1)
