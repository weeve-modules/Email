from calendar import c
from email.mime.base import MIMEBase
import mimetypes
from Google import Create_Service
import base64
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders

CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
file_attachment =[r'/Users/mithila/Documents/raspberry.png']

#create email subject and body
emailMsg = 'Please find the attached documentation'
mimeMessage = MIMEMultipart()
mimeMessage['to'] = 'mithila.ghuge@weeve.network'
mimeMessage['subject'] = 'You won'
mimeMessage.attach(MIMEText(emailMsg, 'plain'))

#Attache file
for attachment in file_attachment:
    content_type,encoding = mimetypes.guess_type(attachment)
    print(content_type)
    main_type, sub_type = content_type.split("/",1)
    print(main_type)
    print(sub_type)
    file_name = os.path.normpath(attachment)
    print(file_name)

    f = open(attachment,'rb')
    print(f.readline())

    myFile = MIMEBase(main_type,sub_type)
    myFile.set_payload(f.read())
    myFile.add_header('Content-Disposition', 'attachment', filename=file_name)
    encoders.encode_base64(myFile)
    
    f.close()
 
    mimeMessage.attach(myFile)

raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

message = service.users().messages().send(
    userId='me',
    body={'raw': raw_string}).execute()

print(message)