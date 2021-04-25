#!/usr/bin/env python
# coding: utf-8

# In[1]:


import warnings
warnings.filterwarnings("ignore")


# In[2]:


from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import mimetypes,sys
import pandas as pd


# In[3]:


from verse_process import *
from mailer_with_attach import *
from ses_mailer import * #sends the html formatted mail from AWS SES
from data_details import * # data details consists of only the spreadsheet_id and the data range. Hidden here for privacy.


# In[4]:


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets' #for reading the subscribers & unsubscribers
          ]


# In[5]:


creds = None    
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('../client_id.json', SCOPES)
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json()) 


# In[6]:


################################ CREATION OF SERVICE ################################ 
service_data_access = build('sheets', 'v4', credentials=creds)
sheet = service_data_access.spreadsheets()
result = sheet.values().get(spreadsheetId=gita_spread_sheet_id , #obtained from data_details,
                                range=gita_data_range).execute()
values = result.get('values', [])
if not values:
    print('No data found.')
else:
    print('DATA FOUND')
    subs_df = pd.DataFrame(data=values,columns=['Email','FName','Phone','Comment','URL'])
    unsubs = sheet.values().get(spreadsheetId=gita_spread_sheet_id , #obtained from data_details,
                                range=unsubscribers).execute().get('values')
    unsubs_series = pd.Series(unsubs,name='Unsubs').apply(lambda x: x[0])


# In[8]:


subs_df['URL'].fillna('https://bhagavadgita.io/chapter/1/verse/1/',inplace=True)


# In[10]:


def url_update(content):
    next_url = 'https://bhagavadgita.io'+str(content.find_all(class_ = 'btn btn-warning btn-rounded waves-effect waves-light')[1].get('href'))
    print('The next URL is : '+next_url)
    if (next_url.find('page')!=-1):
        next_url = url
        
        next_url = next_url[:-3] + '1/'
        
        temp = next_url.split('/')
        temp[-4] = str(int(url.split('/')[-4]) + 1)
        next_url = '/'.join(temp)
        
        print(next_url)
    return next_url


# In[11]:


for i in range(len(subs_df)): #
    print(i)
    if subs_df.loc[i,'Email'] in list(unsubs_series.values):
        print(subs_df.loc[i,'Email'])
        print('Email in unsubscriptions!!')
    else:        
        print(subs_df.loc[i,'Email'])
        url = subs_df.loc[i,'URL']
        print('Current URL is: ' + url)

    #     #fetch verse_data
        content,verse = get_quote(url)
        verse = verse_details(verse,url)


    #     #creation of quote and meaning images
        htm_2_img(verse)
        meaning_img(verse)

    #     #update the URL
        subs_df.loc[i,'URL']=url_update(content)

        subject = 'Shloka for the {}!!'.format('Evening' if datetime.datetime.now().hour > 12 else 'Morning')
        files = ['quote.jpeg','meaning.jpeg']
        BODY_TEXT = ''' This is a placeholder text. '''
        HTML_TEXT = str(open('mail_content.html','r').read()) # to load the quote as html

        HTML_TEXT = HTML_TEXT.format(fname=subs_df.loc[i,'FName'].split(' ')[0].title(),
                         time = 'Evening' if datetime.datetime.now().hour > 12 else 'Morning',
                         chap = verse['chap'].replace('\n',' || '),
                         verse_num = verse['number']              
                        )

        
        print('<<SENDING EMAILS>>')

        service_used = 'SES' # Choose between SES or G-Mail
        if service_used == 'G-Mail':
                # Call the Gmail API
            service_mail = build('gmail', 'v1', credentials=creds)
            sender_email =''
            msg = create_message_with_attachment(sender_email,subs_df.loc[i,'Email'],subject,BODY_TEXT,HTML_TEXT,files)
            send_message(service_mail,'me',msg)

        else:
            print('Done')
            # Incoprate SES based emailing
            ses_emailer(subs_df.loc[i,'Email'],subject,BODY_TEXT,HTML_TEXT,files)
    


# In[12]:


#update next verse URL for each subscriber
values = (tuple(subs_df['URL'].values),tuple())
body = {'majorDimension':'COLUMNS',
        'values': values
       }
result = service_data_access.spreadsheets().values().update(
    spreadsheetId=gita_spread_sheet_id,
    range='Subscribers!F2',
    valueInputOption='USER_ENTERED',
    body=body).execute()
# print('{0} cells updated.'.format(result.get('updatedCells')))
