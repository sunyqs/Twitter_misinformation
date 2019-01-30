import csv 
from twython import Twython 
import pandas as pd
consumer_key='' 
consumer_secret='' 
access_token_key='' 
access_token_secret='' 
twitter = Twython(consumer_key,consumer_secret, access_token_key, access_token_secret)



def get_user_timeline():
    """
    Get all the tweets from the user list timeline
    """
    users = ["TrumpsBlonde", "djt10",
    "NewAutismInfo", "drzimmermann", "SuzorMediation", "Op__Justice","HealthyNews2day", "deb16wood", "joejoe80495073"]
    results = []
    for user in users:
        try:
            results.extend(twitter.get_user_timeline(screen_name=user, count=200))
        except Exception:
            continue
    return results


def to_excel(df, file_name):
    """
    Write file to excel 
    """
    writer = pd.ExcelWriter(file_name)
    df.to_excel(writer,'Sheet1')
    writer.save()


def filter_tweets(results, tweet_set):
    """
    Filter out tweets to only contain the following key words, no RT, no duplicate tweets, 
    and only contains the following fields. 
    """
    data = []
    keywords = ['vaccine', 'vaccines', 'vaccination','vaccinate']
    for tweet in results:
        try:
            if is_valid(tweet, keywords, tweet_set):
                row  = {
                'id': tweet['id'],
                'text': tweet['text'].encode('utf-8'),
                'retweet_count': tweet['retweet_count'], 
                'timestamp' :tweet['created_at'], 
                'media': [], 
                'favorite_count': tweet['favorite_count'], 
                'user_follower_count': tweet['user']['followers_count'],
                'user_id': tweet['user']['id'], 
                'user_screen_name' : tweet['user']['screen_name'].encode('utf-8'),
                'url' : [],
                'hash_tags': []
                }
                data.append(row)
            tweet_set.add(tweet['id'])
        except Exception:
            continue
    return data

def is_valid(tweet, keywords, tweet_set):
    return tweet['id'] not in tweet_set and 'RT' not in tweet['text']  and tweet['text'] in keywords


def get_user_information():
    """
    Get the profile of the user 
    """
    results = {}
    users = ["TrumpsBlonde", "djt10",
    "NewAutismInfo", "drzimmermann", "SuzorMediation", "Op__Justice","HealthyNews2day", "deb16wood", "joejoe80495073"]
    for user in users:
        results['user'] = twitter.show_user(screen_name=user)
    return results


def get_full_tweet(ids):
    """
    Get information of a list of tweet ids
    """
    for i, tweet_id in enumerate(ids):
    try:
        tweet = twitter.show_status(id=str(tweet_id), tweet_mode='extended')
        df_search.set_value(i, 'text', tweet)
    except Exception:
        print(tweet_id)



results = get_user_timeline()
df_search = filter_tweets(results)
df_search = pd.DataFrame(df_search)
tweets = get_full_tweet(df_search['id'])

to_excel(df_search, 'tweets.xlsx')


