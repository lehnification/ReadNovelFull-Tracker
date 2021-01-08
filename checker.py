import requests
import logging
import unidecode
import os
from bs4 import BeautifulSoup
from discord import Webhook, RequestsWebhookAdapter
from utils.save import *


def execute_checks():
    novels = read_config('novels')

    for novel in novels:
        check_file_for_novel(novel)
        chapters = poll_chapters(novel)
        compareSaveWithNewPoll(novel, chapters)


def check_file_for_novel(filename):
    if not file_exists(filename):
        create_file(filename)
        initialize_novel(filename)


def initialize_novel(filename):
    website = read_config('website')
    extenstion = read_config('extenstion')
    link = website + '/' + filename + extenstion

    r = requests.get(link)
    try:
        r.raise_for_status()

        soup = BeautifulSoup(r.content, 'html.parser')
        saving(filename, "name", soup.find(class_='title').text)
        saving(filename, "id", soup.find(id='rating')['data-novel-id'])
        saving(filename, "chapters", poll_chapters(filename))
    except Exception as e:
        logging.exception('Error during initial creation for ' + filename)
        webhook.send(
            user + ' Excpetion occurd during initial creation for ``' + filename + '``.')


def poll_chapters(filename):
    website = read_config('website')
    chapterArchive = read_config('chapterArchive')
    novelId = reading_key(filename, "id")
    link = website + chapterArchive + novelId

    r = requests.get(link)
    try:
        r.raise_for_status()

        soup = BeautifulSoup(r.content, 'html.parser')
        chapters_html = soup.find_all('a')
        chapters = []
        for chapter in chapters_html:
            entry = {}
            entry["name"] = unidecode.unidecode(chapter['title'])
            entry["link"] = website + chapter['href']
            chapters.append(entry)
        return chapters
    except Exception as e:
        logging.exception('Error during chapter poll for ' + filename)
        webhook.send(
            user + ' Excpetion occurd during chapter poll for ``' + filename + '``.')


def compareSaveWithNewPoll(filename, chapters):
    chapters_old = reading_key(filename, "chapters")

    new_chapters = [i for i in chapters if i not in chapters_old]
    if len(new_chapters) != 0:
        saving(filename, "chapters", chapters)
        novel = reading_key(filename, "name")
        for new_chapter in new_chapters:
            webhook.send('**%s**, *%s* \n %s \n %s' % (novel, new_chapter["name"], new_chapter["link"], user))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
    heroku = read_config('heroku')
    webhookId = os.environ['WEBHOOKID'] if heroku else read_config('webhookId')
    webhookToken = os.environ['WEBHOOKTOKEN'] if heroku else read_config('webhookToken')
    webhook = Webhook.partial(webhookId, webhookToken, adapter=RequestsWebhookAdapter())
    discordUserId = os.environ['DISCORDUSERID'] if heroku else read_config('discordUserId')
    user = '<@'+discordUserId+'>'
    execute_checks()
