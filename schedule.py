import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Webhook, RequestsWebhookAdapter
from utils.db import *
from checker import execute_checks


sched = BlockingScheduler()

if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO, format='[%(levelname)s] %(message)s')
    logging.info('--------------')
    logging.info('ReadNovelFull Tracker')
    logging.info('--------------')
    logging.info('Initialise Novels')
    webhookId = get_setting('WEBHOOK_ID')
    webhookToken = get_setting('WEBHOOK_TOKEN')
    webhook = Webhook.partial(webhookId, webhookToken, adapter=RequestsWebhookAdapter())
    discordUserId = get_setting('DISCORD_USER')
    user = '<@'+discordUserId+'>'
    execute_checks()
    sched.add_job(execute_checks, 'cron', minute='0/5')
    sched.start()
