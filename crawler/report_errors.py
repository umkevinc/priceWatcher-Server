import os
import sys
import glob
import argparse
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT


def _main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--date', help='format: YYYY-MM-DD')
    args = parser.parse_args()

    file_list = [] 
    cmd = ['grep', '-Hi', 'Err', '--line-buffer']
    if args.date:
        dt_obj = datetime.strptime(args.date, '%Y-%m-%d')
        file_list = glob.glob('/Users/nasa56_mini/log/*%s_*.txt' % dt_obj.strftime('%Y%m%d'))
    else:
         file_list = glob.glob('/Users/nasa56_mini/log/*.txt')
    if not file_list: 
        return
   
    cmd = ['tail', '-n', '3'] + file_list
    cmd_stdout, cmd_stderr = Popen(cmd, stdout=PIPE, stderr=PIPE).communicate()
    print '[Job Status]'
    print cmd_stdout, cmd_stderr

    cmd = ['grep', '-Hi', 'Err', '--line-buffer'] + file_list
    cmd_stdout, cmd_stderr = Popen(cmd, stdout=PIPE, stderr=PIPE).communicate()
    if cmd_stdout:
        print '[Failed Jobs]'
        print cmd_stdout, cmd_stderr 


if __name__=='__main__':
    sys.exit(_main())
