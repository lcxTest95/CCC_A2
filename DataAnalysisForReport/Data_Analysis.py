# Team 36: Is income and education influence sentiment?
# city: Melbourne Chongxuan Liang - 1118236    
# city: Melbourne Ruitong Liu - 947759
# city: Melbourne Yuhan Zhao  - 1042775
# city: Beijing Zengxu Zhao  - 978084
# city: Melbourne Zhiqi Liu  - 1071551


import json
import re
import csv
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
from wordcloud import WordCloud,ImageColorGenerator
from sklearn.neighbors import KNeighborsClassifier,RadiusNeighborsClassifier
from sklearn.model_selection import cross_val_score
import sklearn.preprocessing as sp
minmax = sp.MinMaxScaler()
#let all characters be lower case
def all_lower(L1):
        return [s.lower() for s in L1 if isinstance(s,str)==True]
#initial the variables
inc_dict={}
edu_dict={}
hashtags=[]
findword=u'(#\w+)+'
coordinates=[]
pol_dict={}
sub_dict={}
pol_avgd={}
sub_avgd={}
point=0
json_dict={}
my_list=[]
count=0
#read the data which got from aurin about incoming
with open('aurin.csv','r') as csvfile:
    reader = csv.reader(csvfile)
    line_num=0
    for line in reader:
            line_num+=1
            if line_num!=1:
                    aurin_sa4=line[0]
                    incoming=line[1]
                    inc_dict[aurin_sa4]=incoming
#read the data which got from aurin about education
with open('aurin2.csv','r') as csvfile:
    reader = csv.reader(csvfile)
    line_num2=0
    for line in reader:
            line_num2+=1
            if line_num2!=1:
                    aurin_sa4=line[0]
                    education=line[2]
                    edu_dict[aurin_sa4]=education
#read the data which got from tweet  
with open("_all_data.json", 'rt', encoding='utf-8') as f2:
    next(f2)
    for i, line in enumerate(f2):
        if line[0]==']':
                break
        #if the trailing exist, then delete 
        elif line[-2] == ',':
                tweet=json.loads(line[:len(line) - 2])
        elif line.endswith('\n'):
                tweet=json.loads(line[:len(line) - 1])
        
        #time=tweet['doc']['tweet_data']['created_at']
        #if we can protect all the tweet after 2020, then this make no sense
        #extract all the hashtags and make a list
        '''
        text=tweet['doc']['tweet_data']['text']
        pattern = re.compile(findword)
        results = pattern.findall(text)
        new_results=all_lower(results)
        hashtags.extend(new_results)
        '''
        #but how do we select the tweet according to the hashtag
        #for instance, we have covid19, quarantine and etc.
        #which is obvious words related to this break
        '''
        try:
                bounding=tweet['tweet_data']['place']['bounding_box']['coordinates']
        except:
                break
        else:
                #calculate the mean value as the coordinate of this user
                if bounding!=None:
                        bounding=np.array(bounding[0])
                        coordinate=np.mean(bounding, axis=0)
                        #print(coordinate)
        '''
        #extract the hashtags
        try:
                directhashtag=tweet['doc']['tweet_data']['entities']['hashtags']
                for i in directhashtag:
                        directhashtags=i['text']
                        hashtags.append(directhashtags.lower())
        except:
                pass
        else:
                count+=1
                tweet_sta4=tweet['doc']['tweet_data']['SA4_CODE']
                polarity=tweet['doc']['tweet_data']['Polarity']
                subjectivity=tweet['doc']['tweet_data']['Subjectivity']
                #put all the useful infomation into dictionaries
                if tweet_sta4!='no_values':
                        pol_dict.setdefault(tweet_sta4,[]).append(polarity)
                        sub_dict.setdefault(tweet_sta4,[]).append(subjectivity)
#calculate the mean value of these two dictionaries
for key, values in pol_dict.items():
        numeric = [float(i) for i in values if isinstance(i,(int,float))]
        pol_avgd[key] = str(round(sum(numeric)/len(numeric),3)) if numeric else values
for key, values in sub_dict.items():
        numeric = [float(i) for i in values if isinstance(i,(int,float))]
        sub_avgd[key] = str(round(sum(numeric)/len(numeric),3)) if numeric else values
        
#find all of SA4
all_sa4=sorted(edu_dict.keys())
#set default value for all of the dictionaries
#46438 is the mean of incoming
for sa4 in all_sa4:
        inc_dict.setdefault(sa4, '46438')
        edu_dict.setdefault(sa4, '0')
        pol_avgd.setdefault(sa4, '0')
        sub_avgd.setdefault(sa4, '0')
#reorder the dict by the key value 
pol_avgd=dict(sorted(pol_avgd.items(), key=lambda x:x[0], reverse=False))
sub_avgd=dict(sorted(sub_avgd.items(), key=lambda x:x[0], reverse=False))
#make a dict for all sa4_dict
for sa4 in all_sa4:
        each_term={}
        #json_dict.setdefault(sa4,{})['inc']=inc_dict[sa4]
        #json_dict.setdefault(sa4,{})['edu']=edu_dict[sa4]
        #json_dict.setdefault(sa4,{})['pol']=pol_avgd[sa4]
        #json_dict.setdefault(sa4,{})['sub']=sub_avgd[sa4]
        #make a list of each sa4
        each_term['sa4']=sa4
        each_term['inc']=round((float(inc_dict[sa4])-36388)/(63510-36388),2)
        each_term['edu']=round((float(edu_dict[sa4])-1.7)/(10.9-1.7),2)
        each_term['pol']=pol_avgd[sa4]
        each_term['sub']=sub_avgd[sa4]
        #set the label for each sa4
        if float(pol_avgd[sa4])>=0.097:
                each_term['rank']='high'
        if float(pol_avgd[sa4])<=0.079:
                each_term['rank']='low'
        if 0.079<float(pol_avgd[sa4])<0.097:
                each_term['rank']='medium'
        my_list.append(each_term)        
#write a json file 
#json_str = json.dumps(json_dict)
#with open('test_data.json', 'w') as json_file:
    #json_file.write(json_str)

#make a csv file for the data
pd.DataFrame(my_list).to_csv('ccc_prj2 .csv')
ana_data=pd.read_csv('ccc_prj2 .csv')
#plot the graph to see the ralationship between 
sns.pairplot(ana_data, x_vars=['inc','edu'], y_vars='pol',kind="reg", height=5, aspect=0.7)
plt.show()

#linear regression
#build the model
X=ana_data.loc[:,('inc','edu')]
y=ana_data.loc[:,'pol']
#split the dataset
X_train,X_test, y_train, y_test = train_test_split(X,y,test_size = 0.2,random_state=0)
print ('X_train.shape={}\ny_train.shape={}\nX_test.shape={}\ny_test.shape={}'.format(X_train.shape,y_train.shape, X_test.shape,y_test.shape))
linreg = LinearRegression()
model=linreg.fit(X_train, y_train)
#print the intercept and coefficients
print (linreg.intercept_)
feature_cols=['inc','edu']
coe=list(zip(feature_cols,linreg.coef_))
print(coe)
#predict the test data
y_pred=linreg.predict(X_test)
print(y_pred)
#calculate the mse rmse and mae
mse_test=np.sum((y_pred-y_test)**2)/len(y_test)
rmse_test=mse_test**0.5
mae_test=np.sum(np.absolute(y_pred-y_test))/len(y_test)
print('MSE:',mse_test)
print('RMSE:',rmse_test)
print('MAE:',mae_test)
#plot the pic to see the difference of the prediction value and the actual value
plt.figure()
plt.plot(range(len(y_pred)),y_pred,'b',label="predict")
plt.plot(range(len(y_pred)),y_test,'r',label="test")
plt.legend(loc="upper right")
plt.xlabel('Incoming and Education')
plt.ylabel('Polarity')
plt.show()

#plot the world cloud of hashtags
hashtag_string=" ".join(hashtags)
wordcloud = WordCloud(background_color="white",width=1500,height=960,margin=10).generate(hashtag_string)
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
print(count)

#k-nn
#split the dataset
Y = ana_data.loc[:,'rank']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=22)
#the model without weights
model1 = KNeighborsClassifier(n_neighbors=8)
model1.fit(X_train, Y_train)
score1 = model1.score(X_test, Y_test)
#the model with the weight of distance
model2 = KNeighborsClassifier(n_neighbors=8, weights='distance')
model2.fit(X_train, Y_train)
score2 = model2.score(X_test, Y_test)
print(score1, score2)
#the results of cross validation
result1 = cross_val_score(model1, X, Y, cv=10)
result2 = cross_val_score(model2, X, Y, cv=10)
print(result1.mean(), result2.mean())
#check how many neighbors is best
neighbors = np.arange(1,9)
train_accuracy=np.empty(len(neighbors))
test_accuracy=np.empty(len(neighbors))
for i,k in enumerate(neighbors):
    #setup a knn classifier with k neighbors
    knn = KNeighborsClassifier(n_neighbors=k)
    #fit the model
    knn.fit(X_train, Y_train)
    #compute accuracy on the training set
    train_accuracy[i] = knn.score(X_train, Y_train)
    #compute accuracy on the test set
    test_accuracy[i] = knn.score(X_test, Y_test)
#plot the pic of the Accuracy of K-NN with Different Numbers of Neighbors
plt.title('Accuracy of K-NN with Different Numbers of Neighbors')
plt.plot(neighbors, test_accuracy, label='Testing Accuracy')
plt.plot(neighbors, train_accuracy, label='Training accuracy')
plt.legend()
plt.xlabel('Number of Neighbors')
plt.ylabel('Accuracy')
plt.show()














