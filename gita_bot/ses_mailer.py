import smtplib  
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import mimetypes,os,base64,random
from aws_ses_creds import * 
'''
This file will contain the following:
    * SENDER : email id of the sender (user@example.com) { Make sure the domain is verifed with DKM settings.}
    * SENDERNAME : name that will appear to the receiver
    * REPLY-EMAIL : mailbox that will monitor your replies
    * USERNAME_SMTP : smtp username from amazon SES
    * PASSWORD_SMTP : smtp password from amazon SES
    * HOST : your region smtp of aws (eg: email-smtp.ap-south-1.amazonaws.com)
    * PORT : the port to be used
'''

def ses_emailer(RECIPIENT,SUBJECT,BODY_TEXT,HTML_TEXT,files):

    '''
    RECIPIENT : a python list object of proposed recipients (if SES is in sandbox, all emails must be verified.)
    SUBJECT: subject of the email.
    BODY_TEXT: The text of the body
    HTML_TEXT: The html content to be embedded. (It somehow overwrites the body_text if put in.)
    files: a python list of files to be attached. 
    '''
    
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
    msg['Bcc'] = RECIPIENT
    msg['reply-to'] = REPLY_EMAIL
    
    part1 = MIMEText(BODY_TEXT, 'plain')

    attachment = './images/k{}.png'.format(random.randint(1,5))

    htm_cnt = (HTML_TEXT[:HTML_TEXT.find('src')] + '''src="cid:{}" '''.format(attachment) + HTML_TEXT[HTML_TEXT.find('alt'):])

    msgText = MIMEText(htm_cnt, 'html') 

    fp = open(attachment, 'rb')                                                    
    img = MIMEImage(fp.read())
    fp.close()
    img.add_header('Content-ID', '<{}>'.format(attachment))

    # Record the MIME types of both parts - text/plain and text/html.
    
    # part2 = MIMEText(HTML_TEXT, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(msgText)

    ## to embed image in html email
    
    msg.attach(img)
    
    for file in files:
        content_type, encoding = mimetypes.guess_type(file)

        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            fp = open(file, 'rb')
            message = MIMEText(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            fp = open(file, 'rb')
            message = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            fp = open(file, 'rb')
            message = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(file, 'rb')
            message = MIMEBase(main_type, sub_type)
            message.set_payload(fp.read())
            fp.close()
        filename = os.path.basename(file)
        message.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(message)

    # Try to send the message.
    try:  
        server = smtplib.SMTP(HOST, PORT)
        server.ehlo()
        server.starttls()
        #stmplib docs recommend calling ehlo() before & after starttls()
        server.ehlo()
        server.login(USERNAME_SMTP, PASSWORD_SMTP)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())
        server.close()
    # Display an error message if something goes wrong.
    except Exception as e:
        print ("Error: ", e)
    else:
        print ("Email sent!")