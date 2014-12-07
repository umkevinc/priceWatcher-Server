import logging
from itertools import chain
from elasticsearch import Elasticsearch

# Set up logging
FORMAT = '[%(asctime)s][%(levelname)s] %(message)s'
logging.basicConfig(format=FORMAT, datefmt='%m-%d-%Y %H:%M:%S')
logging.getLogger().setLevel(logging.INFO)

def bulk_load_es(host, port, es_index, es_doctype, doc_list, opt_dict={}):
	def chunks(lst, chunk_size):
		for i in xrange(0, len(lst), chunk_size):
			yield lst[i:i+chunk_size]

	es = Elasticsearch(host=host, port=port)
	if not opt_dict:
		opt_dict = {
			'index': {
				'_index': es_index, 
				'_type': es_doctype
			}
		}

	if doc_list:
		for sub_list in chunks(doc_list, 100):
			output_body = list(chain(*zip([opt_dict for i in range(len(sub_list))], sub_list)))
			es.bulk(
				index=es_index,
				doc_type=es_doctype,
				body=output_body)
	else:
		logging.warning('Empty data list!')



