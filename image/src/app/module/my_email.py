import re
import smtplib 
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def send_mail(
                log,
                sender="",
                recepients=[],
                subject="",
                msg_body="",
                attachment=[],
                sender_pass = "" 
                ):
    
    log.info("receip",recepients)
    log.info(type(recepients))

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recepients
    msg['Subject'] = subject
    msg.attach(MIMEText(msg_body, 'plain'))
    filename = attachment
    attachment = open(filename, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, sender_pass)
    text = msg.as_string()
    server.sendmail(sender, recepients.split(','), text)
    server.quit()