import os
import sys
import json
import logging
import argparse
from glob import glob

from pricewatcher.tools import ensure_mkdir
from pricewatcher.parser.f21 import ForeverParser
from pricewatcher.utils.load_es import bulk_load_es

# Set up logging
FORMAT = '[%(asctime)s][%(levelname)s] %(message)s'
logging.basicConfig(format=FORMAT, datefmt='%m-%d-%Y %H:%M:%S')
logging.getLogger().setLevel(logging.INFO)

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

def run():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--input-base', default='raw_pages', help='')
    parser.add_argument('--output-base', default='parsed_pages',  help='')
    parser.add_argument('--datetime', required=True, help='YYYYMMDD')
    parser.add_argument('--hour', default='*', help='HH')
    parser.add_argument('--brand', default='*', help='')
    parser.add_argument('--load-es', action='store_true')
    parser.add_argument('--es-host', default='localhost')
    parser.add_argument('--es-port', default='9200')    
    parser.add_argument('--es-cleanup', action='store_true')
    args = parser.parse_args()

    # Argument parsing
    dt_str = args.datetime
    hour_str = args.hour
    brand_str = args.brand
    input_base = args.input_base
    output_base = args.output_base

    # ES arguments
    es_host, es_port = args.es_host, args.es_port    
    load_es = args.load_es

    # Parsing Raw Pages
    input_files = glob(os.path.join(input_base, dt_str, hour_str, brand_str, '*', '*', '*'))    
    for file_path in input_files:        
        dt_str, hour_str, br, category, sub_category, filename = file_path.split('/')[-6:]        
        parser = ForeverParser(file_path)
        doc_list = parser.parse()
        logging.info('[STATUS] parsed %s docs from %s' % (len(doc_list), file_path))
        if not load_es:        
            # Output Result            
            output_dir = os.path.join(output_base, os.path.join(dt_str, hour_str, br, category))
            ensure_mkdir(output_dir)
            output_path = os.path.join(output_dir, filename + '.json')        
            logging.info('[WRITE] output to %s' % output_path)
            with open(output_path, 'w') as ofile:
                ofile.write(json.dumps(doc_list, default=date_handler))
        else:
            es_index, es_doctype = br, category            
            logging.info('[LOAD ES] loading to ElasticSearch...')
            bulk_load_es(es_host, es_port, es_index, es_doctype, doc_list)

