import os
import sys
import logging
import argparse

from pricewatcher.crawler.f21 import ForeverCrawler
from pricewatcher.configs import F21_BASE_URL, F21_CATEGORY_LIST

def run():
    parser = argparse.ArgumentParser(description='Run Crawlers')
    parser.add_argument('--output-dir', default='raw_pages', help='')
    parser.add_argument('--test-run', action='store_true', help='')
    args = parser.parse_args()

    output_dir = args.output_dir
    test_run = args.test_run
    category_list = F21_CATEGORY_LIST if not test_run else F21_CATEGORY_LIST[:3]    
    
    f21_crawler = ForeverCrawler(base_url=F21_BASE_URL,
                                 category_list=category_list,
                                 output_dir=output_dir)
    f21_crawler.run()   	