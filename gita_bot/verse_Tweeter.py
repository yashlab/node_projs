#!/usr/bin/env python
# coding: utf-8

# Posts the verse and meaning images on twitter.

# import all dependencies
import tweepy
import requests,time
from bs4 import BeautifulSoup
import imgkit,datetime
import random,json

from config import *
from verse_process import *


# read from register to fetch today's verse url
url = open('verse_register.txt').read()
url =url.rstrip().split('\n')[-1].split('->')[-1][1:-1]
print('Current URL is: ' + url)

#fetch verse_data
content,verse = get_quote(url)
verse = verse_details(verse,url)
print(verse)

#creation of quote and meaning images
htm_2_img(verse)
meaning_img(verse)
# take a pause
time.sleep(3)

# to build data (you may avoid)
import json
with open("verses/{}_{}.json".format(verse['chap_num'],verse['number']), "w") as outfile: 
    json.dump(verse, outfile)

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

# Create API object
api = tweepy.API(auth)


# In[5]:


# prepare content
status_content = 'ॐ\nChapter {}: {} | {}\nVerse No:{}'.format(verse['chap_num'],
                                              verse['chap'].split('\n')[0],
                                              verse['chap'].split('\n')[1],verse['number'])

hashtags = '\n\n #krishna #iskcon #gita #god #divine #faith #wisdom'


# In[6]:


# Upload image
media1 = api.media_upload("quote.png")
media2 = api.media_upload("meaning.png")
 
# Post tweet with image
tweet = "Python Check"
post_result = api.update_status(status=status_content+hashtags, media_ids=[media1.media_id,media2.media_id])


# In[7]:


#update register for next record
new_url(content)

