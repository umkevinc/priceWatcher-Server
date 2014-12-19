import os
import sys
import logging
import smtplib

# Set up logging
FORMAT = '[%(asctime)s][%(levelname)s] %(message)s'
logging.basicConfig(format=FORMAT, datefmt='%m-%d-%Y %H:%M:%S')
logging.getLogger().setLevel(logging.INFO)


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
        logging.info('[EMAIL] recipients: %s' % to_list)
        logging.info('[EMAIL] subject: %s' % subject)
        logging.info('[EMAIL] msg: %s' % msg)        
        self._smtpserver.sendmail(self._user, to_list, msg)
        self._smtpserver.close()
        logging.info('[EMAIL] Email has sent successfully!') 