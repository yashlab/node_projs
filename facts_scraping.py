#!/usr/bin/env python
# coding: utf-8

# In[8]:


import requests
from bs4 import BeautifulSoup


# In[9]:


url = 'http://randomfactgenerator.net/' # URL to fetch facts
content = requests.get(url) # store the response

tea = BeautifulSoup(content.content,'html.parser') # parse response in html


# In[11]:


# extract facts from the response
fact_dict = {}
i=0
fact_register = open('fact_register.txt','a')
for link in tea.find_all('a',{"class": "twitter-share-button"}):
    fact_dict.update({i:link.get('data-text')})
    fact_register.write(fact_dict[i])
    i+=1
fact_register.close()


# In[13]:


import json
with open("facts.json", "w") as outfile:
    json.dump(fact_dict,outfile)


# In[ ]:




