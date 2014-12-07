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
from pricewatcher.configs import F21_BASE_URL, F21_CATEGORY_LIST
from pricewatcher.crawler.basecrawler import BaseCrawler


logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s][%(levelname)s] %(message)s',
                    datefmt='%y-%m-%d %H:%M')


class ForeverCrawler(BaseCrawler):
    '''
    ForeverCrawler - control what to crawl for Forever21 Site. First generate
    a list of target URLs and then call URLListCrawler to crawl the page.
    '''
    def __init__(self, base_url=F21_BASE_URL, category_list=F21_CATEGORY_LIST, 
                       output_dir='raw_pages'):
        super(ForeverCrawler, self).__init__(base_url, output_dir)        
        self._category_list = category_list        

    def _get_category_info(self, brand, category):
        sniff_params = {
            'br': brand,
            'category': category,
            'pagesize': 120,
            'page': 1,
        }       
        # Set to default
        total_pages = 1
        page_size = 120

        # parsing 
        url = self._base_url + urllib.urlencode(sniff_params)
        logging.info(url)
        html = urlopen_with_retry(url, timeout=60)
        soup = BeautifulSoup(html)

        ul_pnumber = soup.find("ul", {"class": "pagenumber"})
        if ul_pnumber is not None:
            li_list = ul_pnumber.find_all('li', {'class': 'PagerOtherPageCells'})           
            if li_list is not None and len(li_list) > 2:
                last_li = li_list[-2] # Second last li      
                li_href = last_li.find('a', {'class': 'PagerHyperlinkStyle'}).get('href')           
                params = urlparse.parse_qs(urlparse.urlparse(li_href).query)
                params = dict([(k, val[0]) for k, val in params.items()])               
                total_pages, page_size = int(params['page']), int(params['pagesize'])
        return total_pages, page_size

    def _get_category_url_list(self, brand, category, total_pages, page_size):
        target_url_list = []
        logging.info('Generating URL list for brand: %s, category: %s' % (brand, category))
        for pnum in range(1, 1 + total_pages):
            params = {
                'br': brand,
                'category': category,
                'pagesize': page_size,
                'page': pnum
            }                   
            url = self._base_url + urllib.urlencode(params)
            target_url_list.append(url)
        logging.info('Brand=%s, Category=%s, total URLs: %s' % (brand, 
                                                                category, 
                                                                len(target_url_list)))
        return target_url_list

    def _get_url_list(self):
        # Get global url list       
        global_url_list = []
        for br, category in self._category_list:
            total_pages, page_size = self._get_category_info(br, category)
            url_list = self._get_category_url_list(br, 
                                                   category, 
                                                   total_pages, 
                                                   page_size)
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
            params = urlparse.parse_qs(urlparse.urlparse(url).query)
            brand, category = params['br'][0], params['category'][0]            
            output_dir = os.path.join(output_base_dir, 
                                      self._timestamp.strftime('%Y%m%d'),
                                      self._timestamp.strftime('%H'),
                                      'forever21',
                                      brand, 
                                      category)
            ensure_mkdir(output_dir)
            output_path = os.path.join(output_dir,                                     
                                       hashlib.sha224(url).hexdigest())
            logging.info('[WRITE] to %s' % (output_path))
            with open(output_path, 'w') as ofile:               
                ofile.write(url + '\n') 
                ofile.write(html + '\n') 