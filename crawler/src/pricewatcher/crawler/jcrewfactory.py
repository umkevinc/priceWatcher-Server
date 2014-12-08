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
from pricewatcher.configs import JCREWFACTORY_BASE_URL, JCREWFACTORY_CATEGORY_LIST
from pricewatcher.crawler.basecrawler import BaseCrawler


logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s][%(levelname)s] %(message)s',
                    datefmt='%y-%m-%d %H:%M')

class JCrewFactoryCrawler(BaseCrawler):
    '''
    JCrewCrawler - control what to crawl for JCrew Site. First generate
    a list of target URLs and then call URLListCrawler to crawl the page.
    '''
    def __init__(self, base_url=JCREWFACTORY_BASE_URL, category_list=JCREWFACTORY_CATEGORY_LIST, 
                       output_dir='raw_pages'):
        super(JCrewFactoryCrawler, self).__init__(base_url, output_dir)        
        self._category_list = category_list

    def _get_sale_page_number(self):
        #first get total number of pages in sale section. Show 100 items per page.
        sale_page1_url = "https://factory.jcrew.com/search2/index.jsp?N=217&Nloc=en&Ntrm=&Npge=1&Nrpp=100&Nsrt=3&hasSplitResults=false"
        html = urlopen_with_retry(sale_page1_url, timeout=60)
        soup = BeautifulSoup(html)
        total_pnumber = soup.find("span", {"class": "pagination-total"})
        
        # Set to default
        total_pages = 1

        if total_pnumber is not None:
            total_pages= total_pnumber.text         
        return total_pages

    def _get_sale_url_list(self):
        sale_url_list = []
        total_pages = int(self._get_sale_page_number())
        for pnum in range(1, 1 + total_pages):
            sale_url = self._base_url + "search2/index.jsp?N=217&Nloc=en&Ntrm=&Npge=" + str(pnum) + "&Nrpp=100&Nsrt=3&hasSplitResults=false"
            sale_url_list.append(sale_url)
        return sale_url_list

    def _get_category_url_list(self, brand, category):
        target_url_list = []
        #generate url for a brand catagory. Jcrew only has 1 url for each brand catagory.
        logging.info('Generating URL for brand: %s, category: %s' % (brand, category))
        category_url = self._base_url + brand + "/" + category + ".jsp?iNextCategory=-1"    
        logging.info('Brand=%s, Category=%s' % (brand, category))
        target_url_list.append(category_url)
        return target_url_list

    def _get_url_list(self):
        # Get global url list
        global_url_list = self._get_sale_url_list()
        for br, category in self._category_list:
            url_list = self._get_category_url_list(brand=br, category=category)
            global_url_list.extend(url_list)
            logging.info('[STATUS] total URLs: %s' % len(global_url_list))
            # Sleep
            random_sleep(min_t=5, max_t=10)        
        return global_url_list

    def _output(self, page_dict, output_base_dir):
        ''' return None. 
        Writing output to file system. Called by self._crawl

        Arguments: 
            page_dict - dict. key is url and val is html.
            output_base_dir - str. output base dir path.
        '''
        for url, html in page_dict.items():
            _, brand, category = urlparse.urlparse(url).path.split('/')
            category = category[:-4]
            if brand == 'search2':
                brand, category = 'sale', 'all'            
            output_dir = os.path.join(output_base_dir, 
                                      self._timestamp.strftime('%Y%m%d'),
                                      self._timestamp.strftime('%H'),
                                      'jcrewfactory',
                                      brand, 
                                      category)
            ensure_mkdir(output_dir)
            output_path = os.path.join(output_dir,                                     
                                       hashlib.sha224(url).hexdigest())
            logging.info('[WRITE] to %s' % (output_path))
            with open(output_path, 'w') as ofile:               
                ofile.write(url + '\n') 
                ofile.write(html + '\n') 