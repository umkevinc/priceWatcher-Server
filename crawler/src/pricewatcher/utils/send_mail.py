import os
import sys
import smtplib


class PriceWatcherServerMail(object):
    def __init__(self):        
        self._user = 'kcheng.io.host@gmail.com'        
        self._pass = '2014PriceboX'
        self._to_list = ['kevin.cheng76@gmail.com', 'sherry415@gmail.com']
    
        self._smtpserver = smtplib.SMTP('smtp.gmail.com', port=587)
        self._smtpserver.set_debuglevel(1)
        self._smtpserver.ehlo()
        self._smtpserver.starttls()
        self._smtpserver.ehlo
        self._smtpserver.login(self._user, self._pass)

    def send(self, subject, msg, to_list=self._to_list):
        subject = 'To:' + ','.join(to_list) + '\n' + 'From: ' + self._user + '\n'
        print subject
        self._smtpserver.sendmail(self._user, to_list[0], msg)
        self._smtpserver.close()

if __name__=='__main__':
    msg = """success! 
It's good to see this message. :)

Thanks,

Kevin 
"""
    mailer = PriceWatcherServerMail()
    mailer.send(['kevin.cheng76@gmail.com'], 
                 'Testing Server Working Mail',
                 msg)
