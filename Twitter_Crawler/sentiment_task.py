from textblob import TextBlob
from string import punctuation
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import emoji
import re

lmtzr = WordNetLemmatizer()

def preprocess(sentence):
    sent = sentence.lower()
    sent = re.sub('\(via.*\)', '', sent)
    sent = re.sub('(@[^\s]+)', '', sent) ## Remove @ hashtags
    sent = re.sub('\s+', ' ', sent) ## Remove new line characters
    sent = re.sub('\S*@\S*\s?', '', sent) ## Remove Emails
    sent = re.sub("\'", "", sent)  ## Remove distracting single quotes
    sent = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', '', sent) ##Remove urls
    sent = re.sub(r'#([^\s]+)', r'\1', sent) ##Remove # hashtags
    sent = ' '.join(emoji.demojize(sent).replace(":"," ").split())
    sent = re.sub(r'[^\w\s]','',sent) ## Remove punctuation
    sent = [lmtzr.lemmatize(word) for word in word_tokenize(sent)] ## lemmatization
    sent = ' '.join(sent)
    return sent

def sentiment_analyser(tweet_data):
    text = preprocess(tweet_data['text']).lstrip('rt ')
    blob1 = TextBlob(text)
    tweet_data['Polarity'] = blob1.sentiment[0]
    tweet_data['Subjectivity'] = blob1.sentiment[1]
    return tweet_data