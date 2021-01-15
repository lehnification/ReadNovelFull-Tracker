import requests
import logging
import unidecode
import traceback
from bs4 import BeautifulSoup
from discord import Webhook, RequestsWebhookAdapter
from utils.db import *

def execute_checks():
    novels = get_novels()
    for novel in novels:
        try:
            init = check_initialisation(novel)
            if init is None:
                chapters = poll_chapters(novel, novel[2])
                compareSaveWithNewPoll(novel[0], novel[1], novel[3], chapters)
        except Exception as e:
            logging.exception('Error while working on ' + novel[0])
            webhook.send('`%s` threw an error! \n ```python\n%s``` \n %s' % (novel[0], traceback.format_exc(), user))

def check_initialisation(novel):
    if novel[1] is None or novel[2] is None or novel[3] is None:
        initialise_novel(novel[0])
        return True


def initialise_novel(novel):
    link = get_setting('WEBSITE') + '/' + novel + get_setting('EXTENSION')

    r = requests.get(link)
    r.raise_for_status()

    soup = BeautifulSoup(r.content, 'html.parser')
    name = soup.find(class_='title').text
    id = soup.find(id='rating')['data-novel-id']

    if name is None:
        raise ValueError("No title found!")
    if id is None:
        raise ValueError("No novelID found!")

    chapters = poll_chapters(novel, id)
    last_chapter = chapters[len(chapters)-1]["name"]
    insert_novel_initialisation(novel, name, id, last_chapter)
    webhook.send('**%s** initialised \n %s \n %s' % (name, link, user))


def poll_chapters(novel, id):
    website = get_setting('WEBSITE')
    link = website + get_setting('CHAPTER_ARCHIVE') + str(id)

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


def compareSaveWithNewPoll(novel, name, last_chapter, chapters):
    last_index = next((i for i, item in enumerate(chapters) if item["name"] == last_chapter), None)
    new_latest = chapters[len(chapters)-1]
    if last_index is None:
        update_last_chapter(new_latest["name"], novel)
        webhook.send('**%s**, last known chapter *%s* not found in chapter list! \nAdding *%s* as last known chapter \n%s \n%s' % (name, last_chapter, new_latest["name"], new_latest["link"], user))
    else:
        new_chapters = chapters[last_index+1:]
        if len(new_chapters) != 0:
            update_last_chapter(new_latest["name"], novel)
            if len(new_chapters) > 10:
                webhook.send('**%s**, *%s* - *%s* \n %s' % (name, new_chapters[0]["name"], new_chapters[len(new_chapters)-1]["name"], user))
            else:
                for new_chapter in new_chapters:
                    webhook.send('**%s**, *%s* \n %s \n %s' % (name, new_chapter["name"], new_chapter["link"], user))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
    webhookId = get_setting('WEBHOOK_ID')
    webhookToken = get_setting('WEBHOOK_TOKEN')
    webhook = Webhook.partial(webhookId, webhookToken, adapter=RequestsWebhookAdapter())
    discordUserId = get_setting('DISCORD_USER')
    user = '<@'+discordUserId+'>'
    execute_checks()
