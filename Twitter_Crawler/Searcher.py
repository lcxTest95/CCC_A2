import json
import time
from tweepy import OAuthHandler
import twitter_credentials
import geo_task
import tweepy
import Harvester
import couchdb
import requests
import os
import sentiment_task

##############################Twitter Credentials###############################
CONSUMER_KEY = 'fu9wM94fmBBCh8IA0XSzVDJmH'
CONSUMER_SECRET = 'Wj5SzXrD6GVm8UMcMEv05av4ADhLBQyOZmccl7xtqu4kvlITiw'
ACCESS_TOKEN = '1124974628726689794-4jNtG3KWD6u5OuSMcOasvl2SCBQLDX'
ACCESS_SECRET = 'sCPoRHtVFbZnOfUzreIhi0VpoxDXr6kFtQkWU4V20Enl4'

##############################Connect to Twitter API###############################
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# Centre of Melbourne with radius 300 km
melb_geocode = "%f,%f,%fkm" % (-37.817457, 145.002606, 400)
# Centre of Australia with radius 1500 km
au_geocode = "%f,%f,%fkm" % (-25.2743988, 133.7751312, 1500)


USERNAME = 'ccc'
PASSWORD = '90024'
ADDRESS = '172.26.128.112'
PORT = '5984'

def write_couchdb(database_name, id, doc):
    databaseURL = ("http://%s:%s@%s:%s/%s" % (USERNAME, PASSWORD,ADDRESS,PORT,database_name))
    header = {"Content-Type": "application/json"}
    response = requests.put(databaseURL + '/' + str(id), data=json.dumps(doc), headers=header)


def search(geocode, database_name, searchQuery):
    searchQuery = searchQuery  # when search with geocode
    tweetsPerQry = 100  # this is the max the API permits

    # network_error_backoff = 0.25
    # http_error_backoff = 5
    rate_limit_rest = 30
    sinceId = None
    max_id = -1

    while True:
        try:
            new_tweets = api.search(q=searchQuery, count=tweetsPerQry, geocode=geocode, lang='en',
                                    wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                tweet_json = tweet._json
                tweet_geo = geo_task.geo_processing(tweet_json)
                tweet = sentiment_task.sentiment_analyser(tweet_geo)
                _id = tweet["id_str"]
                doc_data = {"_id": _id, "tweet_data": tweet}
                write_couchdb(database_name, _id, doc_data)
                """
                try:
                    db.save(doc_data)
                except couchdb.ResourceConflict as e:
                    #_rev = list(db.get(_id).items())[1][1]
                    db.update(dict(doc_data))
                print(doc_data)
                """
            max_id = new_tweets[-1].id
            print('Finish 100 tweets!!!')
        except tweepy.TweepError as e:
            print("some error : " + str(e))
            time.sleep(rate_limit_rest)
            # if rate limit error happens, let the rest time increase exponentially.
            rate_limit_rest *= 2
    # return res


def get_followers(user_id):
    users = []
    page_count = 0
    for i, user in enumerate(tweepy.Cursor(api.followers, id=user_id, count=200).pages()):
        print('Getting page {} for followers'.format(i))
        users += user
    return users


if __name__ == '__main__':
    database_name = 'twitter_data'
    searchQuery = '*'
    search(au_geocode, database_name, searchQuery)
