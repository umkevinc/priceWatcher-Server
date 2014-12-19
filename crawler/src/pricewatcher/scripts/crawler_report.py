import os
import sys
import glob
import argparse
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT

from pricewatcher.utils.send_mail import PriceWatcherServerMail


def _print_jobs_status(file_list):
    msg = ''
    cmd = ['tail', '-n', '3'] + file_list
    cmd_stdout, cmd_stderr = Popen(cmd, stdout=PIPE, stderr=PIPE).communicate()    
    msg += '[Job Status]\n'
    if len(file_list) == 1:    
        msg += '%s:\n' % file_list[0]    
    msg += '%s\n' % cmd_stdout    
    return msg


def _print_failed_jobs(file_list):
    msg = ''
    cmd = ['grep', '-Hi', 'Err', '--line-buffer'] + file_list
    cmd_stdout, cmd_stderr = Popen(cmd, stdout=PIPE, stderr=PIPE).communicate()
    msg += '[Failed Jobs]\n'
    if cmd_stdout:
        msg += '%s\n'% cmd_stdout        
    else:
        msg += '%s\n' % 'No Failed Jobs!'
    return msg

def run():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--base-dir', default='~/log')
    parser.add_argument('--date', help='format: YYYY-MM-DD')
    parser.add_argument('--email', action='store_true', help='format: YYYY-MM-DD')
    args = parser.parse_args()

    base_dir = args.base_dir
    date_str = args.date
    email_flag = args.email

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
    email_subject = 'PriceWatcher Host - Crawler Status (%s)' % datetime.now().strftime('%Y-%m-%d %H:%M')
    email_content = ''
    email_content += _print_jobs_status(file_list)
    email_content += _print_failed_jobs(file_list)
    print email_subject
    print email_content

    # Send email
    if email_flag:
        mailer = PriceWatcherServerMail()
        mailer.send(email_subject, email_content)