import requests
import logging
import unidecode
import os
import traceback
from bs4 import BeautifulSoup
from discord import Webhook, RequestsWebhookAdapter
from utils.save import *


def execute_checks():
    novels = read_config('novels')

    for novel in novels:
        try:
            check_file_for_novel(novel)
            chapters = poll_chapters(novel, reading_key(novel, "id"))
            compareSaveWithNewPoll(novel, chapters)
        except Exception as e:
            logging.exception('Error while working on ' + novel)
            webhook.send('`%s` threw an error! \n ```python\n%s``` \n %s' % (novel, traceback.format_exc(), user))

def check_file_for_novel(filename):
    if not file_exists(filename):
        initialise_novel(filename)


def initialise_novel(filename):
    link = read_config('website') + '/' + filename + read_config('extenstion')
    data = {"name":"", "id":0, "chapters":[]}

    r = requests.get(link)
    r.raise_for_status()

    soup = BeautifulSoup(r.content, 'html.parser')
    data["name"] = soup.find(class_='title').text
    data["id"] = soup.find(id='rating')['data-novel-id']

    if data["name"] is None:
        raise ValueError("No title found!")
    if data["id"] is None:
        raise ValueError("No novelID found!")

    data["chapters"] = poll_chapters(filename, data["id"])
    create_file(filename, data)
    webhook.send('**%s** initialised \n %s \n %s' % (reading_key(filename, "name"), link, user))


def poll_chapters(filename, novelId):
    website = read_config('website')
    link = website + read_config('chapterArchive') + novelId

    r = requests.get(link)
    r.raise_for_status()

    soup = BeautifulSoup(r.content, 'html.parser')
    chapters_html = soup.find_all('a')
    if len(chapters_html) == 0:
        raise ValueError("No chapters found!")
    chapters = []
    for chapter in chapters_html:
        entry = {}
        entry["name"] = unidecode.unidecode(chapter['title'])
        entry["link"] = website + chapter['href']
        chapters.append(entry)
    return chapters


def compareSaveWithNewPoll(filename, chapters):
    chapters_old = reading_key(filename, "chapters")

    new_chapters = [i for i in chapters if i not in chapters_old]
    if len(new_chapters) != 0:
        saving(filename, "chapters", chapters)
        novel = reading_key(filename, "name")
        if len(new_chapters) > 15:
            webhook.send('**%s**, *%s* - *%s* \n %s' % (novel, new_chapters[0]["name"], new_chapters[len(new_chapters)-1]["name"], user))
        else:
            for new_chapter in new_chapters:
                webhook.send('**%s**, *%s* \n %s \n %s' % (novel, new_chapter["name"], new_chapter["link"], user))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    heroku = read_config('heroku')
    webhookId = os.environ['WEBHOOKID'] if heroku else read_config('webhookId')
    webhookToken = os.environ['WEBHOOKTOKEN'] if heroku else read_config('webhookToken')
    webhook = Webhook.partial(webhookId, webhookToken, adapter=RequestsWebhookAdapter())
    discordUserId = os.environ['DISCORDUSERID'] if heroku else read_config('discordUserId')
    user = '<@'+discordUserId+'>'
    execute_checks()
