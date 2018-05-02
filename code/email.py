## Sending Email Alerts
#
#
import smtplib

server = smtplib.SMTP_SSL('smtp.gmail.com',port=465) #server for sending the email

server.ehlo() # simple starting of the connection
server.login('username','password') # login credentials and password

msg = """From:username@gmail.com
Subject: Test Email \n
To: recipient_email@gmail.com \n
/--- This is where the email content goes. It could be information about the error, time of day, where in the script, etc. ---/"""

server.sendmail('your@gmail.com','παραλήπτης@gmail.com',msg) # this is where the email is sent to the recipient

server.quit() # exit the connection
