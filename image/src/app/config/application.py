"""
All constants specific to the application
"""
from app.utils.env import env
from app.utils.floatenv import floatenv


APPLICATION = {
    "INPUT_LABEL": env("INPUT_LABEL", "temperature"),
    "SENDER_EMAIL_ID":env("SENDER_EMAIL_ID", "xyz@gmail.com"),
    "RECIPENT_EMAIL_ID": env("RECIPENT_EMAIL_ID", "abc@gmail.com"),
    "EMAIL_SUBJECT": env("EMAIL_SUBJECT", "Daily status report"),
    "EMAIL_BODY": env("EMAIL_BODY", "Data point {{label}} reached the value of {{value}} {{unit}} at {{time}}"),
    "ATTACHMENT_FILE_PATH": env("ATTACHMENT_FILE_PATH", "xxx"),
    "SENDER_PASS":env("SENDER_PASS", "*****")
}