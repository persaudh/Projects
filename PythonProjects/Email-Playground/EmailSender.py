import smtplib
from email.message import EmailMessage
import os 
from dotenv import load_dotenv

load_dotenv()

address = os.getenv("EmailAddress")
pwd = os.getenv("EmailPWD")


# with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:  
#     email_address = address
#     email_password = pwd
#     connection.login(email_address, email_password )
#     connection.sendmail(from_addr=email_address, to_addrs=email_address, 
#     msg="subject:hi \n\n this is my message")


# email_from = address
# email_to = address
# email_message = "subject:hi \n\n this is my message"
# with smtplib.SMTP_SSL(host="smtp.gmail.com",port=465) as smtp:
#     smtp.login(address,pwd)
#     smtp.sendmail(from_addr=email_from,to_addrs=email_to,msg=email_message) 
#     print("Email Sent!")

email_from = address
email_to = address
email_message = "subject:Testing automated email \n\n his is an email sent from Python!"



with smtplib.SMTP(host="smtp.gmail.com",port=587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login(address,pwd)
    smtp.sendmail(from_addr=email_from,to_addrs=email_to,msg=email_message)
    print("Email Sent!")