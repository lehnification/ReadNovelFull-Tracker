import logging
import subprocess
import sys
from apscheduler.schedulers.blocking import BlockingScheduler
from utils.save import read_config

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=15)
def timed_job():
    p = subprocess.call([sys.executable, 'checker.py'])

if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
    logging.info('--------------')
    logging.info('ReadNovelFull Chapter Checker')
    logging.info('--------------')
    sched.start()
