import smtplib 
from email.message import EmailMessage

msg = EmailMessage()
msg["Subject"] = "Email Testing"
msg["From"] = "Weeve GmbH"
msg["To"] = "mithila.ghuge@weeve.network"
msg.set_content("test email from mithila")

server = smtplib.SMTP_SSL('smtp.gmail.com',465)
server.login("miths0512989@gmail.com", "TestEmailWeeve@1234")
server.send_message(msg)
server.quit()