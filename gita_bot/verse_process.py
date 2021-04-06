#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import imgkit,datetime
import random,json


# In[2]:


def get_quote(url):
    '''
    Note: Credits for the absolutely amazing content goes to https://bhagavadgita.io/.
    It wouldn't have been possible without them.
    '''
    
#     print('ENG URL:{}'.format(url))
    url_hindi = url + 'hi/'
#     print('HIN URL:{}'.format(url_hindi))
    content = requests.get(url)
    content_hindi = requests.get(url_hindi)

    english_tea = BeautifulSoup(content.content,'html.parser') # parse response in html
    hindi_tea = BeautifulSoup(content_hindi.content,'html.parser') # parse response in html

    # type(tea.find_all('div',{"class":'sanskrit-text'}))
    verse = english_tea.find_all(class_ = 'verse-sanskrit')[0].get_text()
    verse_transliteration = english_tea.find_all(class_ = 'verse-transliteration')[0].get_text()
    verse_word_meanings_eng = english_tea.find_all(class_='verse-word')[0].get_text()
    verse_meanings_eng = english_tea.find_all(class_='verse-meaning')[0].get_text()
    verse_word_meanings_hindi = hindi_tea.find_all(class_='verse-word')[0].get_text()
    verse_meanings_hindi = hindi_tea.find_all(class_='verse-meaning')[0].get_text()
    return english_tea, {'0':verse,
            '1':verse_transliteration,
            '2':verse_meanings_hindi,
            '3':verse_meanings_eng,
            '4':verse_word_meanings_eng,
            '5':verse_word_meanings_hindi}


# In[3]:


def htm_2_img(verse):
    import random
    background_colors = ['#ffb703','#E072A4','#ef476f','#43aa8b','#264653','#2A9D8F','#E9C46A','#F4A261']
    krishna_pics = ['images/k'+str(i)+'.svg' for i in range(1,6)]
    html_cont = """
    <!DOCTYPE html>
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            <meta name="charset" content="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0">
            <style>
                .section-head{                
                    font-weight: bold;
                    text-align: center;
                    font-size: 25px;               
                }

                .sanskrit-text{                
                    text-align: center;
                    font-size: 1.6rem;
                    font-weight: bolder;
                    padding-bottom: 10px;
                    background-color: #ffb703;
                }

                .transliter{
                    text-align: center;                
                    font-style: italic;
                    font-size: 1.6rem;
                    padding-bottom: 10px;
                    font-family: 'Noto Serif';
                }

                .grid-container {
                    display: grid;
                    grid-template-columns: 550px 550px;
                    padding: 10px;
                    margin-top: 10px;                
                    align-content: center;
                }

                .grid-item {

                    bottom: 50%;
                    padding: 10px;                
                    text-align: center; 
                    border-radius: 0.8em;
                    
                }

                .grid-title {                
                    border: 2px solid #00743f;
                    border-radius: 0.8em;
                    padding: 5px;
                    font-size: 1.2em;
                    text-align: center;
                    grid-column-start: 1;
                    grid-column-end: 3;
                    }

                * 
                {
                    background-color:""" + str(random.choice(background_colors)) + """;

                }   

                .body_style {
                    width: 1200px;
                    height: 600px;
                    border: 2px solid #f9f9f9;
                    border-radius: 0.8em;
                    align-self: center;
                }

                hr {
                    width: 25%;
                    height: 2px;
                    align-self: center;
                    background-color: #ef476f;
                    border:0px
                }        

            </style>

        </head>

        <body class="body_style">

            <section id = 'shlok'>

                <div class="grid-container">
                    <div class="grid-title" style = "color: #e05330;">||<u>श्लोक</u>|| </div>                  

                    <div class="grid-item sanskrit-text"> """ + verse['0'].rstrip().replace('\n','<br>') + """                
                    </div>
                    <hr>

                    <div class="grid-item transliter"> """ + verse['1'].rstrip().replace('\n','<br>') + """
                    </div>
                </div>


            </section>


            <section>
                <div class="grid-container">
                    <div class="grid-title">
                        <b style="color: #1DA1F2;font-size: 18px;">Translation</b>
                    </div>

                    <div class="grid-item" style="font-size: 18px;">
                        <div style="color: #dc2f02;"> <b> English</b></div> """ + verse['3'] + """                    
                    </div>
                    <hr>
                    <div class="grid-item" style="font-size: 18px;">
                        <div style="color: #dc2f02;"> <b> हिंदी</b></div> """ + verse['2'] + """                    
                    </div>                   

                </div>
                <div style="text-align: center;">
                    <img src='""" + random.choice(krishna_pics) + """' alt="" style="height: 50px; width: 50px;">
                </div>
            </section>

        </body>
    </html>

    """
    with open('verse_html.html','w') as f:
        f.write(html_cont)
    f.close()
    
    imgkit.from_file('verse_html.html','quote.png')


# In[4]:


def meaning_img(verse):
    html_cont = """
    <!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <meta name="charset" content="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0">
        <style>
            .grid-container {
                display: inline-grid;
                align-content: center;
                grid-template-columns: 300px 300px;
                background-color: #ffcad4;
                
            }

            .grid-item {
                bottom: 50%;
                padding: 10px;                
                text-align: center; 
                border-radius: 0.8em; 
                font-size: 1.3rem;
                border:2px solid #cc2936;
                margin-top: 5px;
                /* width: 50%; */
                
            }
            

        </style>
            
    </head>
    <body>
        <div class = 'grid-container'>
            <div class="grid-item" style="grid-column-end:3; grid-column-start: 1;"> <b> Word Meanings || शब्दार्थ </b> </div>
            <span>
                <div class="grid-item">""" + str(verse['4'].rstrip().replace('; ','<br>')) + """
                </div>
                <div class="grid-item"> """ + str(verse['5'].replace('(','<br>(')) + """
                </div>
            </span>            
        </div>        
    </body>
</html>
    
    """
    
    with open('word_mean.html','w') as f:
        f.write(html_cont)
    f.close()
    
    imgkit.from_file('word_mean.html','meaning.png')


# In[5]:


#obatain next url
def new_url(content):
    next_url = 'https://bhagavadgita.io'+str(content.find_all(class_ = 'btn btn-warning btn-rounded waves-effect waves-light')[1].get('href'))
    print('The next URL is : '+next_url)
    if (next_url.find('page')!=-1):
        next_url = url
        
        next_url = next_url[:-3] + '1/'
        
        temp = next_url.split('/')
        temp[-4] = str(int(url.split('/')[-4]) + 1)
        next_url = '/'.join(temp)
        
        print(next_url)
        
    with open('verse_register.txt','a') as obj:
        obj.write("{}->'{}'\n".format(datetime.date.today(),str(next_url)))
        print('''Written to file: {}->'{}'\n '''.format(datetime.date.today(),str(next_url)))
    obj.close()
    


# In[6]:


def verse_details(verse):
    with open('chap_details.json','r') as f:
        chap = json.load(f)
    ver_num = url.split('/')[-2]
    ver_chap = chap[url.split('/')[-4]]
    
    verse.update({'chap':ver_chap,'number':ver_num})
    return verse
    


# In[7]:


import time

url = open('verse_register.txt').read()
url =url.rstrip().split('\n')[-1].split('->')[-1][1:-1]
print('Current URL is: ' + url)
content,verse = get_quote(url)
verse = verse_details(verse)
print(verse)
new_url(content)
htm_2_img(verse)
meaning_img(verse)
time.sleep(3)
    


# In[8]:


import json
with open("current_verse.json", "w") as outfile: 
    json.dump(verse, outfile)


# In[ ]:




