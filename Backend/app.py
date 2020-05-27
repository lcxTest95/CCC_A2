# Team 36: Is income and education influence sentiment?
# city: Melbourne Chongxuan Liang - 1118236    
# city: Melbourne Ruitong Liu - 947759
# city: Melbourne Yuhan Zhao  - 1042775
# city: Beijing Zengxu Zhao  - 978084
# city: Melbourne Zhiqi Liu  - 1071551


from flask import Flask, redirect, url_for, request,jsonify,Response
import json
from couchdb import design
import couchdb
import sys
import requests
import json
import time
import ast
import socket
from flask_cors import *

USERNAME = 'ccc'
PASSWORD = '90024'

ADDRESS = '172.26.128.112'
PORT = '5984'

tweet_db_name = 'twitter_data'
tweet_design = 'tweet_stats'     #information of couchdb account


def get_view_as_dic(view_name, db_name, design_name, group_level):
   databaseURL = ("http://%s:%s@%s:%s/%s/_design/%s/_view/%s" % (USERNAME, PASSWORD, ADDRESS, PORT, tweet_db_name, design_name, view_name))
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


def creatdic(webdic):
   server = couchdb.Server("http://%s:%s@%s:%s" % ('ccc', '90024', ADDRESS, '5984'))
   db1 = server['incoming']
   db2 = server['education']
   addlist = []
   inclist = []
   edulist = []
   diction = {}
   a = 0
   for inc in db1:
      addlist.append(inc)
      inclist.append(db1[inc]["inc"])
      edulist.append(db2[inc]["edu"])
   inclist.append("0")
   edulist.append(db2["901"]["edu"])
   addlist.append('901')
   for item in addlist:
      diction[item] = {}
   for itme in inclist:
      diction[addlist[a]]["inc"] = inclist[a]
      a = a + 1
   a = 0
   for item in edulist:
      diction[addlist[a]]["edu"] = edulist[a]
      a = a + 1
   a = 0
   for item1 in webdic:
      for item2 in diction:
         if item1 == item2:
            diction[item2]["pol"] = str(webdic[item1]['polarity_stats']["avg"])
            diction[item2]["pol1"] = str(round((webdic[item1]['polarity_stats']["avg"]), 3))
            diction[item2]["hashtag1"] = "#" + webdic[item1]['hashtag'][0][0]
            diction[item2]["hashtag2"] = "#" + webdic[item1]['hashtag'][1][0]
            diction[item2]["hashtag3"] = "#" + webdic[item1]['hashtag'][2][0]
            a = a + 1
   j = diction
   # print(j)
   return j


def fulldata():
   ## Get the mapreduce result from view
   twitter_total_count_dic = get_view_as_dic('sumOfTweets', tweet_db_name, tweet_design, 1)
   twitter_polarity_dic = get_view_as_dic('polarity_stats', tweet_db_name, tweet_design, 2)
   twitter_subjectivity_dic = get_view_as_dic('subjectivity_stats', tweet_db_name, tweet_design, 2)
   twitter_hashtag_dic = get_view_as_dic('hashtag_sum', tweet_db_name, tweet_design, 2)

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

   # print(to_web_dic)
   dic = creatdic(to_web_dic)
   # print(dic)
   # print("Start Sleeping")
   # time.sleep(rest_time)
   return dic


print("start here")
dic1 = fulldata()
print(dic1)
print(type(dic1))
dic = str(dic1)
print(dic)
print(type(dic))
dic = dic.replace("\'","\"")
print(dic)
print(type(dic))
dic = ast.literal_eval(dic)
print(type(dic))  #transform ' in dictionary to "


app = Flask(__name__)
CORS(app, resources=r'/*')   #allow visit from other url

@app.route('/')
def hello_world():

    return request.args.__str__()

@app.route('/admin')  # when visit  http://127.0.0.1:5000/admin
def hello_admin():
   # return 'Hello Admin'
   data= dic1
   print(type(data))
   print(data)
   # return (jsonify((data)))
   # return jsonify(dic)
   #return jsonify(json.dumps(dic1))
   return jsonify(dic1)
@app.route('/guest/<guest>')
def hello_guest(guest):
   return 'Hello %s as Guest' % guest


@app.route('/user/<name>')
def hello_user(name):
   if name =='admin':
      return redirect(url_for('hello_admin'))
   else:
      return redirect(url_for('hello_guest',guest = name))


if __name__ == '__main__':
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   s.connect(("8.8.8.8", 80))
   ip = s.getsockname()[0]
   s.close()
   app.run(debug = False, host = ip)
