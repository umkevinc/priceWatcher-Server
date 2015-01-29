import os
import sys
import logging
import argparse
import urlparse
from pprint import pprint
from bs4 import BeautifulSoup
from datetime import datetime


logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s][%(levelname)s] %(message)s',
                    datefmt='%y-%m-%d %H:%M')


class ForeverParser(object):    
    def __init__(self, file_path):
        self._file_path = file_path        
        self._url, self._soup = self._read_file(file_path)
        self._brand, self._category, self._sub_category = self._file_path.split('/')[-4:-1]
        self._record_datetime = datetime.strptime(
                                    ''.join(self._file_path.split('/')[4:6]), 
                                    '%Y%m%d%H')

    def _read_file(self, file_path):
        url, soup = None, None
        with open(file_path, 'r') as ifile: 
            url = ifile.readline().strip()
            soup = BeautifulSoup(ifile.read())
        return url, soup    

    def parse(self):
        item_list = []  
        category_list = self._soup.find("table", {'class': 'dlCategoryList'})
        if not category_list: return item_list
        
        cells = category_list.find_all('table')     
        if not cells: return item_list

        for cell in cells:
            sold_out = cell.find('div', {'class': lambda L: L and L.startswith('ItemImage') and L.endswith('S')}) 
            img_div = cell.find('div', {'class': lambda L: L and L.startswith('ItemImage')})                
            page_url = img_div.find('a', {'class': 'pdpLink'}).get('href')              
            img_url = img_div.find('a', {'class': 'pdpLink'}).find('img').get('src')            
            item_name = cell.find('div', {'class': 'DisplayName'}).text
            original_price = cell.find('font', {'class': 'oprice'})
            item_price = cell.find('font', {'class': 'price'}).text.strip().split('$')[-1]

            params = urlparse.parse_qs(urlparse.urlparse(page_url).query)
            product_id = params['ProductID']
            doc = {
                'brand': self._brand,
                'category': self._category,
                'sub_category': self._sub_category,
                'product_id': product_id[0],
                'img_url': img_url,
                'page_url': page_url,
                'item_name': item_name,
                'price': item_price,
                'datetime': self._record_datetime,
            }
            if sold_out:
                doc['sold_out'] = True
            if original_price:
                doc['original_price'] = original_price.text.strip().split('$')[-1]            
            item_list.append(doc)            
        return item_list    

