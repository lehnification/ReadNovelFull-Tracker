import logging
import requests
import traceback
import unidecode
import utils.settings as settings
from bs4 import BeautifulSoup
from discord import Webhook, RequestsWebhookAdapter
from utils.db import *
from utils.webhook import triggerWebhook

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
            triggerWebhook('`%s` threw an error! \n ```python\n%s```' % (novel[0], traceback.format_exc()))

def check_initialisation(novel):
    if novel[1] is None or novel[2] is None or novel[3] is None:
        initialise_novel(novel[0])
        return True


def initialise_novel(novel):
    link = settings.website + '/' + novel + settings.extension

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
    triggerWebhook('**%s** initialised \n %s' % (name, link))


def poll_chapters(novel, id):
    link = settings.website + settings.chapterArchive + str(id)

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
        entry["link"] = settings.website + chapter['href']
        chapters.append(entry)
    return chapters


def compareSaveWithNewPoll(novel, name, last_chapter, chapters):
    last_index = next((i for i, item in enumerate(chapters) if item["name"] == last_chapter), None)
    new_latest = chapters[len(chapters)-1]
    if last_index is None:
        update_last_chapter(new_latest["name"], novel)
        triggerWebhook('**%s**, last known chapter *%s* not found in chapter list! \nAdding *%s* as last known chapter \n%s' % (name, last_chapter, new_latest["name"], new_latest["link"]))
    else:
        new_chapters = chapters[last_index+1:]
        if len(new_chapters) != 0:
            update_last_chapter(new_latest["name"], novel)
            if len(new_chapters) > 10:
                triggerWebhook('**%s**, *%s* - *%s*' % (name, new_chapters[0]["name"], new_chapters[len(new_chapters)-1]["name"]))
            else:
                for new_chapter in new_chapters:
                    triggerWebhook('**%s**, *%s* \n %s' % (name, new_chapter["name"], new_chapter["link"]))
