"""
All logic related to the module's main application
Mostly only this file requires changes
"""
from email.mime.base import MIMEBase
import mimetypes
from app.module.Google import Create_Service
import base64
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import socket
import json
import time
from app.config import APPLICATION

# Set module settings
__INPUT_LABEL__ = APPLICATION['INPUT_LABEL']
__RECIPENT_EMAIL_ID__ = APPLICATION['RECIPENT_EMAIL_ID']
__EMAIL_SUBJECT__ = APPLICATION['EMAIL_SUBJECT']
__EMAIL_BODY__ = APPLICATION['EMAIL_BODY']
__ATTACHMENT_FILE_PATH__ = APPLICATION['ATTACHMENT_FILE_PATH']

def module_main(data,log):
    """
    Implement module logic here. Although this function returns data, remember to implement
    egressing method to external database or another API.

    Args:
        data ([JSON Object]): [Data received by the module and validated by data_validation function]

    Returns:
        [string, string]: [data, error]
    """

    now = time.localtime()
    current_time = time.strftime("%H:%M:%S", now)
    try:
        parsed_data = data[__INPUT_LABEL__]
        device_name = socket.gethostname()
        with open('client_secret.json','w') as fd :
            fd.write(APPLICATION['AUTH_TOKEN'])
        log.info("file created" )
        with open('client_secret.json','r') as fd :
            log.info(fd.readlines())
        CLIENT_SECRET_FILE = 'client_secret.json'
        API_NAME = 'gmail'
        API_VERSION = 'v1'
        SCOPES = ['https://mail.google.com/']
        log.info("before service")
        service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES, log=log)
        log.info("1st point")
        file_attachment = [r'__ATTACHMENT_FILE_PATH__']
        log.info("2nd point")
 

       # This is a way to format the data in a way that Slack can understand.
        replacement_dict = {
            '{{time}}': str(current_time),
            '{{value}}':  str(parsed_data),
            '{{label}}':  __INPUT_LABEL__,
            '{{device_name}}': str(device_name),
        }

        email_message = __EMAIL_BODY__
        for key, value in replacement_dict.items():
            email_message = email_message.replace(key, value)

        email_body = json.dumps({'text': email_message})
        log.info(email_body)

        #create email subject and body
        emailMsg = email_body
        mimeMessage = MIMEMultipart()
        mimeMessage['to'] = __RECIPENT_EMAIL_ID__
        mimeMessage['subject'] = __EMAIL_SUBJECT__
        mimeMessage.attach(MIMEText(emailMsg, 'plain'))

        #Attache file
        for attachment in file_attachment:
            content_type,encoding = mimetypes.guess_type(attachment)
            main_type, sub_type = content_type.split("/",1)
            file_name = os.path.normpath(attachment)

        f = open(attachment,'rb')
        log.info("checkpoint3")
        myFile = MIMEBase(main_type,sub_type)
        myFile.set_payload(f.read())
        myFile.add_header('Content-Disposition', 'attachment', filename=file_name)
        encoders.encode_base64(myFile)
    
        f.close()
 
        mimeMessage.attach(myFile)
        log.info("checkpoint4")

        raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
        log.info("checkpoint5")
        message = service.users().messages().send(
        userId='me',
        body={'raw': raw_string}).execute()

        log.info(message)

    except Exception as e:
        return None, f"Unable to perform the module logic {e}" 
