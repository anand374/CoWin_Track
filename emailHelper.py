#!/usr/bin/env python
# coding: utf-8

import smtplib, ssl
import email.message

m = email.message.Message()
port = 465  # For SSL
password = ""

sender_email = ""
receiver_email = ""


# Create a secure SSL context
context = ssl.create_default_context()

def getMessage(sender_email,receiver_email,msg):
    m['From'] = sender_email
    m['To'] = receiver_email
    m['Subject'] = "Vaccine is Available!"
    m.set_payload(msg)
    return str(m)

def getErrorMessage(sender_email,receiver_email,msg):
    m['From'] = sender_email
    m['To'] = receiver_email
    m['Subject'] = "Vaccine script Error!"
    m.set_payload(msg)
    return str(m)

def sendMail(msg):
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        # TODO: Send email here
        
        server.sendmail(sender_email, receiver_email, getMessage(sender_email,receiver_email,msg))


def sendErrorMail(msg):
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        
        server.sendmail(sender_email, receiver_email, getErrorMessage(sender_email,receiver_email,msg))