import os
import sys
import glob
import argparse
from datetime import datetime


def run():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--base-dir', default='/Users/nasa56_mini/log')
    parser.add_argument('-d', '--date', help='format: YYYY-MM-DD')
    args = parser.parse_args()

    base_dir = args.base_dir
    date_str = args.date

    log_files = []
    if date_str:
        dt_obj = datetime.strptime(date_str, '%Y-%m-%d')
        log_files = glob.glob(os.path.join(base_dir, 
                                           '*%s_*.txt' % dt_obj.strftime('%Y%m%d')))
    else:
        log_files = glob.glob(os.path.join(base_dir, 
                                           '*.txt'))

    for log_file in log_files:
        base_dir, filename = os.path.split(log_file)
        br, _, dt, _ = filename[:-4].split('_')
        year, month = dt[:4], dt[4:6]
        new_path = os.path.join(base_dir, br, year, month, filename)
        os.rename(log_file, new_path)
        if os.path.exists(new_path):
            print 'moved: %s -> %s' % (log_file,  new_path)
        else:
            sys.stderr.write('Failed: moving from %s -> %s' % (log_file, new_path))
            sys.exit()  
