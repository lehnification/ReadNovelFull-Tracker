import logging
import subprocess
import sys
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=15)
def timed_job():
    p = subprocess.call([sys.executable, 'checker.py'])

if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO, format='[%(levelname)s] %(message)s')
    logging.info('--------------')
    logging.info('ReadNovelFull Tracker')
    logging.info('--------------')
    logging.info('Initialise Novels')
    p = subprocess.call([sys.executable, 'checker.py'])
    logging.info("Switching over to 15 minutes interval check")
    sched.start()
