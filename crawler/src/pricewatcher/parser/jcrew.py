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


class JcrewParser(object):    
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
        item_list, price_list = [], []
        prod_container = self._soup.find('div', {'id': 'productContainer'})
        if not prod_container: return item_list

        prod_section = prod_container.find('section', {'class': 'product-section'})
        if not prod_section: return item_list

        cells = prod_section.find_all('figure', {'class': 'product-item'})
        if not cells: return item_list

        for cell in cells:
            product_id = cell.get('data-productid')
            basecode = cell.get('data-basecode')

            a_tag = cell.find('a', {'class': 'product-image-wrap'})
            page_url = a_tag.get('href')
            img_url = a_tag.find('img')['src']
                    
            figcaption_tag = cell.find('figcaption')            
            item_name = figcaption_tag.find('div', {'class': 'product-name'}).text.strip()            
            original_price = figcaption_tag.find('div', {'class': 'product-price-was'})
            item_price = float(figcaption_tag.find('span', {'class': 'product-sale-price'}).text.strip().split('$')[-1])
            promote_text = figcaption_tag.find('div', {'class': 'promo-badge'})

            product_swatches_tag = cell.find('div', {'class': 'product-swatches'})
            is_freeshipping = True if cell.find('div', {'class': 'product-free-shipping'}) is not None else False

            # Can't get data from source code
            # color_names, color_codes, color_imgs = [], [], []            
            # imgs = product_swatches_tag.find_all('img')
            # for img in imgs:
            #     color_names.append(img.get('data-colorname'))
            #     color_codes.append(img.get('data-colorcode'))
            #     color_imgs.append(img.get('src'))                

            #Product Information
            doc = {                
                'brand': self._brand,
                'category': self._category,
                'sub_category': self._sub_category,
                'product_id': product_id,
                'basecode': basecode,                
                'img_url' : img_url,
                'page_url': page_url,
                'item_name': item_name,                
                'is_freeshipping': is_freeshipping,
                'datetime': self._record_datetime,
                'price': item_price,
                # 'color_names': color_names,
                # 'color_codes': color_codes,
                # 'color_imgs': color_imgs
            }
            

            # Price information
            price_doc = {                
                'product_id': product_id,
                'basecode': basecode,
                'datetime': self._record_datetime,
                'price': item_price,
            }
            if original_price:
                doc['original_price'] = float(original_price.text.strip().split('$')[-1])
                doc['price_off'] = doc['original_price'] - doc['price']                
                doc['perct_price_off'] = 1.0*(doc['original_price'] - doc['price'])/doc['original_price']
                price_doc['original_price'] = float(original_price.text.strip().split('$')[-1])
            if promote_text:
                doc['promo_text'] = promo_text.text.strip()
                price_doc['promo_text'] = promo_text.text.strip()
                
            price_list.append(price_doc)
            item_list.append(doc)
        return item_list, price_list
        
