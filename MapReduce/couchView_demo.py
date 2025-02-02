# Team 36: Is income and education influence sentiment?
# city: Melbourne Chongxuan Liang - 1118236    
# city: Melbourne Ruitong Liu - 947759
# city: Melbourne Yuhan Zhao  - 1042775
# city: Beijing Zengxu Zhao  - 978084
# city: Melbourne Zhiqi Liu  - 1071551

from couchdb import design
import couchdb
import sys
import requests
import json
import time

USERNAME = 'ccc'
PASSWORD = '90024'

ADDRESS = '172.26.128.112'
PORT = '5984'

tweet_db_name = 'twitter_data'
tweet_design = 'tweet_stats'

rest_time = 900

def get_view_as_dic(view_name, db_name, design_name, group_level):
    databaseURL = ("http://%s:%s@%s:%s/%s/_design/%s/_view/%s" % (
    USERNAME, PASSWORD, ADDRESS, PORT, tweet_db_name, design_name, view_name))
    headerss = {"Content-Type": "application/json"}
    parameters = {'reduce': 'true', 'group_level': group_level}
    res = {}
    with requests.get(databaseURL, params=parameters, stream=True) as response:
        results = response.json()['rows']
    return results


def sort_hashtag(to_web_dic):
        for area in to_web_dic.keys():
                if 'hashtag' not in to_web_dic[area]:
                        continue
                hashtag = to_web_dic[area]['hashtag']
                tmp = sorted(hashtag.items(), key=lambda d: d[1], reverse=True)
                if len(tmp) < 3:
                        to_web_dic[area]['hashtag'] = tmp
                else:
                        to_web_dic[area]['hashtag'] = tmp[:3]
        return to_web_dic

while True:
        ## Get the mapreduce result from view
        twitter_total_count_dic = get_view_as_dic('sumOfTweets', tweet_db_name, tweet_design, 1)
        twitter_polarity_dic = get_view_as_dic('polarity_stats', tweet_db_name, tweet_design, 2)
        twitter_subjectivity_dic = get_view_as_dic('subjectivity_stats', tweet_db_name, tweet_design, 2)
        twitter_hashtag_dic = get_view_as_dic('hashtag_sum', tweet_db_name, tweet_design,2)

        to_web_dic = {}

        for doc in twitter_total_count_dic:
            if doc['key'][0] in to_web_dic.keys():
                to_web_dic[doc['key'][0]]['total_count'] = doc['value']
            else:
                to_web_dic[doc['key'][0]] = {}
                to_web_dic[doc['key'][0]]['total_count'] = doc['value']
        for doc in twitter_polarity_dic:
            if doc['key'] in to_web_dic.keys():
                to_web_dic[doc['key']]['polarity_stats'] = doc['value']
            else:
                to_web_dic[doc['key']] = {}
                to_web_dic[doc['key']]['polarity_stats'] = doc['value']

        for doc in twitter_hashtag_dic:
                ## sort the hashtag for each area
                if doc['key'][0] not in to_web_dic.keys():
                        to_web_dic[doc['key'][0]] = {}
                if 'hashtag' not in to_web_dic[doc['key'][0]].keys():
                        to_web_dic[doc['key'][0]]['hashtag'] = {}
                to_web_dic[doc['key'][0]]['hashtag'][doc['key'][1]] = doc['value']

        to_web_dic = sort_hashtag(to_web_dic)
        print("Start Sleeping")
        time.sleep(rest_time)




