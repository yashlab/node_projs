from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import mimetypes
from mailer_with_attach import *
from data_details import * # data details consists of only the spreadsheet_id and the data range. Hidden here for privacy.

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send' , #for sending emails,
          'https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/spreadsheets.readonly' #for reading the subscribers
          ]

def main():
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
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_id.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service_mail = build('gmail', 'v1', credentials=creds)
    service_data_access = build('sheets', 'v4', credentials=creds)

    sheet = service_data_access.spreadsheets()
    result = sheet.values().get(spreadsheetId=gita_spread_sheet_id , #obtained from data_details,
                                range=gita_data_range).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print(values)
        # for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            # print('{}--{}'.format(row[0], row[1]))


    # Create a list of emails
    email_list = ''
    for i in values:
        email_list = email_list + i[0] + ','
    email_list = email_list[:-1] 
    

    # Call the Gmail API
    msg = create_message_with_attachment('yashlaboratoire@gmail.com',email_list,'OAuth Based E-Mail','This is sent via app and VS!!',['quote.png','meaning.png'])
    send_message(service_mail,'me',msg)

if __name__ == '__main__':
    main()



