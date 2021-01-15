import utils.settings as settings
from discord import Webhook, RequestsWebhookAdapter

def initWebhook(id, token):
    return Webhook.partial(id, token, adapter=RequestsWebhookAdapter())

def triggerWebhook(message):
    settings.webhook.send('%s\n%s' % (message, settings.user))