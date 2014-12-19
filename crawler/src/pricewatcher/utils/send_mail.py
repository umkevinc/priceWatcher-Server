import os
import sys
import smtplib


class PriceWatcherServerMail(object):
    '''
    Example.
    msg = "This is a test message"
    mailer = PriceWatcherServerMail()
    mailer.send(['kevin.cheng76@gmail.com'], 
                 'Testing Server Working Mail',
                 msg)
    '''

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

    def send(self, subject, msg, to_list=None):
        to_list = self._to_list if to_list is None else to_list
        subject = 'To:' + ','.join(to_list) + '\n' + 'From: ' + self._user + '\n'
        print subject
        self._smtpserver.sendmail(self._user, to_list[0], msg)
        self._smtpserver.close()