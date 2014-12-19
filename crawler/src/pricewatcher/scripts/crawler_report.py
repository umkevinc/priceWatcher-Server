import os
import sys
import glob
import argparse
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT


def _print_jobs_status(file_list):
    cmd = ['tail', '-n', '3'] + file_list
    cmd_stdout, cmd_stderr = Popen(cmd, stdout=PIPE, stderr=PIPE).communicate()
    print '[Job Status]'
    print cmd_stdout, cmd_stderr


def _print_failed_jobs(file_list):
    cmd = ['grep', '-Hi', 'Err', '--line-buffer'] + file_list
    cmd_stdout, cmd_stderr = Popen(cmd, stdout=PIPE, stderr=PIPE).communicate()
    print '[Failed Jobs]'
    if cmd_stdout:    
        print cmd_stdout, cmd_stderr 
    else:
        print 'No Failed Jobs!'


def run():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--base-dir', default='~/log')
    parser.add_argument('--date', help='format: YYYY-MM-DD')
    args = parser.parse_args()

    base_dir = args.base_dir
    date_str = args.date

    # Generate the file list
    file_list = []    
    if date_str:
        dt_obj = datetime.strptime(date_str, '%Y-%m-%d')
        file_list = glob.glob(os.path.join(base_dir, 
                                           '*%s_*.txt' % dt_obj.strftime('%Y%m%d')))
    else:
         file_list = glob.glob(os.path.join(base_dir,
                                            '*.txt'))
    if not file_list: 
        return

    # Print status
    _print_jobs_status(file_list)
    _print_failed_jobs(file_list)