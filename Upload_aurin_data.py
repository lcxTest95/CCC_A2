import couchdb
import csv
import json
import requests
username='ccc'
password='90024'
address='172.26.128.112'
port='5984'
inc_dict={}
edu_dict={}
def write_couchdb(database_name,aid,adict):
    databaseURL=('http://%s:%s@%s:%s/%s' %(username,password,address,port,database_name))
    header={'Content-Type':'application/json'}
    response=requests.put(databaseURL+'/'+str(aid),data=json.dumps(adict),headers=header)

with open('aurin.csv','r') as csvfile:
    reader = csv.reader(csvfile)
    line_num=0
    for line in reader:
            line_num+=1
            if line_num!=1:
                    inc_data={}
                    aurin_sa4=line[0]
                    incoming_value=line[1]
                    inc_dict[aurin_sa4]=incoming_value
                    incid=aurin_sa4
                    inc_data={'id':incid,'inc':incoming_value}
                    write_couchdb('incoming',incid,inc_data)

with open('aurin2.csv','r') as csvfile:
    reader = csv.reader(csvfile)
    line_num2=0
    for line in reader:
            line_num2+=1
            if line_num2!=1:
                    edu_data={}
                    aurin_sa4=line[0]
                    education_level=line[2]
                    edu_dict[aurin_sa4]=education_level
                    eduid=aurin_sa4
                    edu_data={'id':eduid,'edu':education_level}
                    write_couchdb('education',eduid,edu_data)
