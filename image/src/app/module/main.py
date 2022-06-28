"""
All logic related to the module's main application
Mostly only this file requires changes
"""

from app.config import APPLICATION
from app.module.my_email import send_mail
import time
import socket

__INPUT_LABEL__ = APPLICATION["INPUT_LABEL"]
__EMAIL_BODY__ = APPLICATION["EMAIL_BODY"]

# Set module settings
def module_main(data,log):
    """
    Implement module logic here. Although this function returns data, remember to implement
    egressing method to external database or another API.

    Args:
        data ([JSON Object]): [Data received by the module and validated by data_validation function]

    Returns:
        [string, string]: [data, error]
    """

    try:
        parsed_data = data[__INPUT_LABEL__]
        recepients = APPLICATION['RECIPENT_EMAIL_ID']
        # if ',' in recepients:
        #     recepients = recepients.split(',')
        attachment = APPLICATION['ATTACHMENT_FILE_PATH']
        # if ',' in attachment:
        #     attachment = attachment.split(',')

        now = time.localtime()
        current_time = time.strftime("%H:%M:%S", now)
        device_name = socket.gethostname()

        def msg_body(parsed_data,current_time,device_name,__INPUT_LABEL__,__EMAIL_BODY__):
           
            # This is a way to format the data in a way that Slack can understand.
            replacement_dict = {
                '{{time}}': str(current_time),
                '{{value}}':  str(parsed_data),
                '{{label}}':  __INPUT_LABEL__,
                '{{device_name}}': str(device_name),
            }

            email_body = __EMAIL_BODY__
            for key, value in replacement_dict.items():
                email_body = email_body.replace(key, value)

            #slack_data = json.dumps({'text': alert_message})
            return email_body

        send_mail(
            log,
            sender=APPLICATION['SENDER_EMAIL_ID'],
            recepients=recepients,
            subject=APPLICATION['EMAIL_SUBJECT'],
            msg_body=msg_body(parsed_data,current_time,device_name,__INPUT_LABEL__,__EMAIL_BODY__),
            attachment= attachment,
            sender_pass=APPLICATION['SENDER_PASS'], 
            )
        
        return parsed_data, None

    except Exception as e:
        return None, f"Unable to perform the module logic {e}" 
