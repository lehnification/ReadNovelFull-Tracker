from utils.db import get_setting
from utils.webhook import initWebhook

def init():
    global webhook
    global user
    global website
    global extension
    global chapterArchive

    webhookId = get_setting('WEBHOOK_ID')
    webhookToken = get_setting('WEBHOOK_TOKEN')
    webhook = initWebhook(webhookId, webhookToken)

    userId = get_setting('DISCORD_USER')
    user = '<@%s>' % userId

    website = get_setting('WEBSITE')
    extension = get_setting('EXTENSION')
    chapterArchive = get_setting("CHAPTER_ARCHIVE")