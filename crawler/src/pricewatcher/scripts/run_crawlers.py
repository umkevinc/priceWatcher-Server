import os
import sys
import logging
import argparse

from pricewatcher.crawler.f21 import ForeverCrawler
from pricewatcher.configs import F21_BASE_URL, F21_CATEGORY_LIST

def run():
    parser = argparse.ArgumentParser(description='Run Crawlers')
    parser.add_argument('--output-dir', default='raw_pages', help='')
    args = parser.parse_args()

    output_dir = args.output_dir

    f21_cralwer = ForeverCrawler(base_url=F21_BASE_URL,
                                 category_list=F21_CATEGORY_LIST,
                                 output_dir=output_dir)
    f21_cralwer.run()   	