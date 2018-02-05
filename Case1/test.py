import tweepy

auth = tweepy.OAuthHandler('Rs8Ba8b7AOL7IDVIHljuVBERC', '84xMvqAD4dfndq29a4RzarCUufdJ9hBHZKcLctqayJXRH6LbLA')
auth.set_access_token('389922744-Km3NZ6rShZqSHZ3ZPh24lLBSVxGVqybX8r5B57f8', 'lJDLpjjyx9QwcCffCJZr4dYKo7aqNwdO7skbjeHxJWZLs')

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print tweet.text
