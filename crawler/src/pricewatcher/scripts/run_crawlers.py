import os
import sys
import logging
import argparse

from pricewatcher.crawler.jcrew import JCrewCrawler
from pricewatcher.crawler.f21 import ForeverCrawler
from pricewatcher.crawler.jcrewfactory import JCrewFactoryCrawler
from pricewatcher.crawler.anntaylor import AnnTaylorCrawler
from pricewatcher.crawler.zara import ZaraCrawler

from pricewatcher.configs import F21_BASE_URL, F21_CATEGORY_LIST
from pricewatcher.configs import JCREW_BASE_URL, JCREW_CATEGORY_LIST
from pricewatcher.configs import JCREWFACTORY_BASE_URL, JCREWFACTORY_CATEGORY_LIST
from pricewatcher.configs import ANN_TAYLOR_BASE_URL
from pricewatcher.configs import ZARA_BASE_URL, ZARA_CATEGORY_LIST

def run():
    parser = argparse.ArgumentParser(description='Run Crawlers')
    parser.add_argument('--output-dir', default='raw_pages', help='')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--f21', action='store_true', help='run foever21 crawler')
    group.add_argument('--jcrew', action='store_true', help='run jcrew crawler')
    group.add_argument('--jcrewfactory', action='store_true', help='run jcrewfactory crawler')
    group.add_argument('--ann', action='store_true', help='run ann taylor crawler')
    group.add_argument('--zara', action='store_true', help='run zara crawler')
    group.add_argument('--all', action='store_true', help='run all crawlers')
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
                                     category_list=category_list,
                                     output_dir=output_dir)
        jcrew_crawler.run()

    if args.jcrewfactory or args.all:
        category_list = JCREWFACTORY_CATEGORY_LIST if not test_run else JCREWFACTORY_CATEGORY_LIST[:3]    
        jcrewfactory_crawler = JCrewFactoryCrawler(base_url=JCREWFACTORY_BASE_URL,
                                     category_list=category_list,
                                     output_dir=output_dir)
        jcrewfactory_crawler.run()

    if args.ann or args.all:
        ann_taylor_crawler = AnnTaylorCrawler(base_url=ANN_TAYLOR_BASE_URL, 
                                              output_dir=output_dir,
                                              test_run=test_run)
        ann_taylor_crawler.run()

    if args.zara or args.all:
        category_list = ZARA_CATEGORY_LIST if not test_run else ZARA_CATEGORY_LIST[:3]    
        zara_crawler = ZaraCrawler(base_url=ZARA_BASE_URL,
                                     category_list=category_list,
                                     output_dir=output_dir)
        zara_crawler.run()
