
# Srimad Bhagvad Gita Bot
While discovering the twitter API and observing my mother reading SBG, I thought to build upon something in the intersection. However, it turned out to be much more 
engaging than my expectations.
I would really like to thank: [Bhagvad Gita](https://bhagavadgita.io/). This would surely not been possible without it.

### Tech and Concepts:
- Web Scraping using Python (Beautiful Soup).
- MIME (Multipurpose Internet Mail Extensions) Mail structure.
- Working of a SMTP servers.
- Using AWS Simple Email Service (SES) for bulk emails.
- Using ```tweepy``` python library to access twitter API.
- Little bit of HTML and CSS styling.


> NOTE: Make sure you are in the Gita bot directory before running any scripts. 
> ## Process:
 1. Verse_Tweeter.py
	- Dependency:
		* config.py
		* verse_process.py
	- Functions:
		* loads the verse data from source
		* generates html and images for verse and meanings
		* updates the register with today date and next verse URL
		 
2. mailstart.py
	- Dependency:
		- mailer_with_attach.py : 
		- data_details.py
		- ses_mailer.py
	- Functions:
		- fetches the recipients list from Google Sheets API.
		- sends emails to the recipients using either G-Mail or Amazon SES.

## Sample Outputs

![](quote.jpeg)
![](meaning.jpeg)

## Inner .py Scripts Details:
- verse_process.py
    * obtain all verse information in a ```json``` in verses folder. for eg. ```1_1.json``` 
    * generate html pages that are rendered by imgkit module and mailers.
- mailer_with_attach.py
    * holds function for sending different styles of emails via G-Mail API.
    * text, audio, video, image type attachments are supported.
- ses_mailers.py
    * send email via SES as a service (or gmail if required.. update ```service_type``` in code.)
    * support functionalities of ```mailer_with_attach.py```.
    * there might be some custom changes that you need to do to meet your requirements. However, baseline code is same and depends mainly on correctly building the MIMEMulipart mail.


### Private Files
- config.py : Holds information of twitter API access credentials.
- client_id.json : Holds Google API credentials.
- aws_ses_creds.py: AWS SES credentials in additon to the Sender Name and custom domain sender id.
- data_details.py: Holds spreadsheet id and data ranges for your data in Google Spreadsheets.
- token.json: created automatically to connect to google APIs in future once OAuth authentication is successful. 
