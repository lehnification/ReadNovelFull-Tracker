import logging
import subprocess
import sys
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

sched = BlockingScheduler()

def timed_job():
    p = subprocess.call([sys.executable, 'checker.py'])

if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO, format='[%(levelname)s] %(message)s')
    logging.info('--------------')
    logging.info('ReadNovelFull Tracker')
    logging.info('--------------')
    logging.info('Initialise Novels')
    timed_job()
    sched.start()
    sched.add_job(timed_job, 'cron', minute='0/5')
