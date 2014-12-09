import os
import sys
import socket
import urllib
import hashlib
import logging
import urlparse
from time import sleep
from urllib2 import URLError
from bs4 import BeautifulSoup

from pricewatcher.tools import ensure_mkdir
from pricewatcher.tools import urlopen_with_retry, random_sleep
from pricewatcher.configs import ANN_TAYLOR_BASE_URL, ANN_TAYLOR_CATEGORY_LIST
from pricewatcher.crawler.basecrawler import BaseCrawler


logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s][%(levelname)s] %(message)s',
                    datefmt='%y-%m-%d %H:%M')


class AnnTaylorCrawler(BaseCrawler):
    '''    
    '''
    def __init__(self, base_url=ANN_TAYLOR_BASE_URL, category_list=ANN_TAYLOR_CATEGORY_LIST, 
                 output_dir='raw_pages', test_run=False):
        super(AnnTaylorCrawler, self).__init__(base_url, output_dir)
        self._category_list = [cat_name.lower() for cat_name in category_list]
        self._test_run = test_run

    def _get_sub_category_url(self, url_suffix):
        catid = url_suffix.strip('/').split('/')[-1]
        page_size = 101
        params = {
            'trail': '',
            'pageSize': page_size,
            'gridSize': 'md',
            'catid': catid,
            'goToPage': 1, 
            'viewAll': 'viewAll',
            'Request': True
        }
        url = '%s/%s?%s' % (self._base_url, url_suffix, urllib.urlencode(params))        
        html = urlopen_with_retry(url, timeout=60)
        soup = BeautifulSoup(html)
        yield url
        
        # Parse total
        ol = soup.find('ol', {'class': 'pages'})
        if ol is not None:
            lis = ol.find_all('li')
            if lis is not None and len(lis) > 2:
                total_pages = int(lis[-2].text)                
                for i in range(2, total_pages + 1):
                    params['goToPage'] = i
                    url = '%s/%s?%s' % (self._base_url, url_suffix, urllib.urlencode(params))
                    yield url

    def _get_categories(self):
        ''' Return a dict
        key: category name
        value: category link
        '''
        url = self._base_url
        logging.info(url)
        # Reading the Homepage
        html = urlopen_with_retry(url, timeout=60)
        soup = BeautifulSoup(html)
        category_list = []

        nav_site = soup.find('div', {'id': 'nav-site'})
        ul_l1 = nav_site.find('ul', {'class', 'list-l1'})
        # Loop Through Main Category 
        cat_cnt = 0
        for li in ul_l1.find_all('li'):
            cat_div = li.find('div', {'class': 'changeCategorys'})
            if cat_div is not None:
                if self._test_run and cat_cnt > 1: break
                cat_name = cat_div.a.text.strip()
                if cat_name.lower() not in self._category_list: continue
                ul_l2 = li.find('ul', {'class': 'list-l2'})
                # Loop Through Sub Category
                for sub_li in ul_l2.find_all('li'):
                    if sub_li.a is not None:
                        sub_cat_name = sub_li.text.strip().replace(' ', '_')
                        href = sub_li.a.get('href')
                        for url in  self._get_sub_category_url(href):                            
                            yield cat_name, sub_cat_name, url
                    random_sleep(min_t=3, max_t=5)
                cat_cnt += 1

    def _get_url_list(self):
        # Get global url list               
        global_url_list = []
        category_list = self._get_categories()
        for cat_name, sub_cat_name, url in category_list:
            logging.info('Reading Category: %s, %s' % (cat_name, sub_cat_name))
            logging.info('Retrieved URL: %s' % (url))            
            global_url_list.append((cat_name, sub_cat_name, url))                                  
            logging.info('Total pages: %s' % len(global_url_list))

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
                                      'anntaylor',
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
