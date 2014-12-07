import os
import sys
import logging
import argparse

from pricewatcher.crawler.jcrew import JCrewCrawler
from pricewatcher.crawler.f21 import ForeverCrawler
from pricewatcher.configs import F21_BASE_URL, F21_CATEGORY_LIST
from pricewatcher.configs import JCREW_BASE_URL, JCREW_CATEGORY_LIST

def run():
    parser = argparse.ArgumentParser(description='Run Crawlers')
    parser.add_argument('--output-dir', default='raw_pages', help='')
    parser.add_argument('--f21', action='store_true', help='run foever21 crawler')
    parser.add_argument('--jcrew', action='store_true', help='run jcrew crawler')
    parser.add_argument('--all', action='store_true', help='run all crawlers')
    parser.add_argument('--test-run', action='store_true', help='')
    args = parser.parse_args()

    output_dir = args.output_dir
    test_run = args.test_run

    if args.f21 or args.all:
        category_list = F21_CATEGORY_LIST if not test_run else F21_CATEGORY_LIST[:3]    
        f21_cralwer = ForeverCrawler(base_url=F21_BASE_URL,
                                     category_list=category_list,
                                     output_dir=output_dir)
        f21_cralwer.run()

    if args.jcrew or args.all:
        category_list = JCREW_CATEGORY_LIST if not test_run else JCREW_CATEGORY_LIST[:3]    
        jcrew_crawler = JCrewCrawler(base_url=JCREW_BASE_URL,
                                     category_list=JCREW_CATEGORY_LIST,
                                     output_dir=output_dir)
        jcrew_crawler.run()