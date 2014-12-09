import os
import time
import errno
import random
import urllib
import urllib2
import logging
import contextlib

from time import sleep
from functools import wraps
from urllib2 import URLError


logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s][%(levelname)s] %(message)s',
                    datefmt='%y-%m-%d %H:%M')


def ensure_mkdir(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


class RandomTimeGenerator(object):
	def __init__(self, max_t=20, min_t=10):
		self._max = max_t	
		self._min = min_t

	def get_rnd_time(self):
		sec = random.randrange(self._min, self._max)		
		return sec


def retry(ExceptionToCheck, tries=4, delay=3, backoff=2, logger=None):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param ExceptionToCheck: the exception to check. may be a tuple of
        exceptions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """
    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                #except ExceptionToCheck, e:
                except Exception, e:    
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print msg
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry


@retry(URLError, tries=3, delay=10, backoff=2)
def urlopen_with_retry(url, timeout):
	'''
	urlopen with retry
	'''
	with contextlib.closing(urllib2.urlopen(url, timeout=timeout)) as connection:
		html = connection.read()
	return html


def random_sleep(min_t=3, max_t=5):
	timer = RandomTimeGenerator(max_t=max_t,  min_t=min_t)	
	sleep_time = timer.get_rnd_time()
	logging.info('[sleep] %s sec...' % sleep_time)
	sleep(sleep_time)