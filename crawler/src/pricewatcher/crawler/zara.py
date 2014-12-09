import os
import sys
import socket
import urllib
import hashlib
import logging
import urlparse
from time import sleep
from bs4 import BeautifulSoup

from pricewatcher.tools import ensure_mkdir
from pricewatcher.tools import urlopen_with_retry, random_sleep
from pricewatcher.configs import ZARA_BASE_URL, ZARA_CATEGORY_LIST
from pricewatcher.crawler.basecrawler import BaseCrawler


logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s][%(levelname)s] %(message)s',
                    datefmt='%y-%m-%d %H:%M')

class ZaraCrawler(BaseCrawler):
    '''
    ZaraCrawler - control what to crawl for Zara Site. First generate
    a list of target URLs and then call URLListCrawler to crawl the page.
    '''
    def __init__(self, base_url=ZARA_BASE_URL, category_list=ZARA_CATEGORY_LIST, 
                       output_dir='raw_pages'):
        super(ZaraCrawler, self).__init__(base_url, output_dir)        
        self._category_list = category_list

    def _get_category_url_list(self, brand, category):
        category_url_list = []
        #generate url for a brand catagory. Zara only has 1 url for each brand catagory.
        logging.info('Generating URL for brand: %s, category: %s' % (brand, category))
        category_url = self._base_url + "us/en/" + brand + "/" + category + ".html"    
        logging.info('Brand=%s, Category=%s' % (brand, category))
        category_url_list.append((brand, category, category_url))
        return category_url_list

    def _get_url_list(self):
        # Get global url list
        global_url_list = []
        for brand, category in self._category_list:
            category_url_list = self._get_category_url_list(brand, category)
            global_url_list.extend(category_url_list)
            logging.info('[STATUS] total URLs: %s' % len(global_url_list))
            # Sleep
            random_sleep(min_t=5, max_t=10)        
        return global_url_list

    def _output(self, cat_name, sub_cat_name, page_dict, output_base_dir):
        ''' return None. 
        Writing output to file system. Called by self._crawl

        Arguments: 
            page_dict - dict. key is url and val is html.
            output_base_dir - str. output base dir path.
        '''        
        for url, html in page_dict.items():            
            output_dir = os.path.join(output_base_dir, 
                                      self._timestamp.strftime('%Y%m%d'),
                                      self._timestamp.strftime('%H'),
                                      'zara',
                                      cat_name,
                                      sub_cat_name)
            ensure_mkdir(output_dir)
            output_path = os.path.join(output_dir,                                     
                                       hashlib.sha224(url).hexdigest())
            logging.info('[WRITE] to %s' % (output_path))
            with open(output_path, 'w') as ofile:               
                ofile.write(url + '\n') 
                ofile.write(html + '\n') 

    def _crawl(self, target_urls):
        progress = 0 
        for cat_name, sub_cat_name, url in target_urls:
            inventory = {}
            logging.info('[STATUS] Fetching page %s' % url)
            try:
                html = urlopen_with_retry(url, timeout=60)
                inventory.update({url: html})       
                progress += 1

                # Writing Output
                self._output(cat_name, sub_cat_name, inventory, self._output_dir)   
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
            logging.info('[PROGRESS] success: %s, failed: %s, total: %s' % (progress, 
                                                                            len(self._failed_url_list),
                                                                            len(target_urls)))
        logging.info('[STATUS] Finished crawling all pages: (%s / %s)' % (progress, 
                                                                          len(target_urls)))
        logging.info('with %s URLs failed.' % len(self._failed_url_list))
