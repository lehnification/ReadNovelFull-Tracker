import logging
import utils.settings as settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from checker import execute_checks
from discord import Webhook, RequestsWebhookAdapter
from utils.webhook import triggerWebhook



sched = BlockingScheduler()

if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO, format='[%(levelname)s] %(message)s')
    logging.info('--------------')
    logging.info('ReadNovelFull Tracker')
    logging.info('--------------')
    logging.info('Initialise Settings')
    settings.init()
    logging.info('Initialise Novels')
    execute_checks()
    sched.add_job(execute_checks, 'cron', minute='0/5')
    sched.start()
