import os
import sys
import socket
import urllib
import urllib2
import hashlib
import logging
import urlparse

from time import sleep
from random import shuffle
from urllib2 import URLError
from bs4 import BeautifulSoup
from datetime import datetime

from pricewatcher.tools import urlopen_with_retry, random_sleep
from pricewatcher.tools import ensure_mkdir, RandomTimeGenerator


class BaseCrawler(object):
    def __init__(self, base_url, output_dir):
        self._base_url = base_url
        self._output_dir = output_dir
        self._timestamp = datetime.now()

        self._target_url_list = []
        self._failed_url_list = []

    def _get_url_list(self):
        raise NotImplementedError("Subclasses should implement this!")

    def _output(self, page_dict, output_base_dir):
        raise NotImplementedError("Subclasses should implement this!")

    def _crawl(self, target_urls):
        progress = 0 
        for url in target_urls:
            inventory = {}
            logging.info('[STATUS] Fetching page %s' % url)
            try:
                html = urlopen_with_retry(url, timeout=60)
                inventory.update({url: html})       
                progress += 1

                # Writing Output
                self._output(inventory, self._output_dir)   
                logging.info('[STATUS] Done crawling page :%s' % (url))
                # Sleep
                random_sleep(min_t=5, max_t=10)

            except URLError, e:
                logging.error("Oops, timed out? %s" % url)
                logging.error(str(e))
                self._failed_url_list.append(url)
                sleep(25)

            except socket.timeout:
                logging.error("Timed out!")
                self._failed_url_list.append(url)           
                sleep(25)

            except:
                logging.error("Unknown Error!")
                self._failed_url_list.append(url)           
                sleep(25)
            logging.info('[PROGRESS] success: %s, failed: %s, total: %s' % (progress, 
                                                                            len(self._failed_url_list),
                                                                            len(target_urls)))
        logging.info('[STATUS] Finished crawling all pages: (%s / %s)' % (progress, 
                                                                          len(target_urls)))
        logging.info('with %s URLs failed.' % len(self._failed_url_list))

    def run(self):
        self._target_url_list = self._get_url_list()
        shuffle(self._target_url_list)

        # First Crawl
        self._crawl(self._target_url_list)

        # Retry untill no failure cases
        cnt = 1
        while(self._failed_url_list):
            logging.info("Retry %s time for failed URLs:" % cnt)
            logging.info("Numbers of failed URLs: %s" % len(self._failed_url_list))
            new_url_list, self._failed_url_list  = self._failed_url_list, []            
            self._crawl(new_url_list)
            logging.info("Done %s time crawling!" % cnt)
            cnt += 1