import asyncio
import json
import logging
import os
import sys


def read_json(file_name):
    with open('json/' + file_name + '.json', 'r') as f:
        try:
            cont = json.load(f)
            return cont
        except:
            return None


def reading_key(file_name, searched):
    with open('json/' + file_name + '.json', 'r') as f:
        cont = json.load(f)
        try:
            return cont[searched]
        except:
            return None


def read_config(searched):
    return reading_key("config", searched)

def saving(file_name, field, value):
    with open('json/' + file_name + '.json', 'r') as q:
        content = json.load(q)
        secure_content = content
        with open('json/' + file_name + '.json', 'w') as f:
            try:
                content[field] = value
                f.seek(0)
                f.truncate()
                json.dump(content, f, indent=4, separators=(',', ':'))
                return True
            except Exception as e:
                f.seek(0)
                f.truncate()
                json.dump(secure_content, f, indent=4, separators=(',', ':'))
                logging.error("An Error occurd while saving")
                return e


async def save_config(field, value):
    with await lock:
        return await loop.run_in_executor(None, saving, 'config', field, value)


def deleting_key(file_name, key):
    with open('json/' + file_name + '.json', 'r') as q:
        content = json.load(q)
        secure_content = content
        with open('json/' + file_name + '.json', 'w') as f:
            try:
                del content[key]
                f.seek(0)
                f.truncate()
                json.dump(content, f, indent=4, separators=(',', ':'))
                return True
            except Exception as e:
                f.seek(0)
                f.truncate()
                json.dump(secure_content, f, indent=4, separators=(',', ':'))
                logging.error("An Error occurd while saving")
                return e


async def delete_key(file_name, key):
    with await lock:
        return await loop.run_in_executor(None, deleting_key, file_name, key)


def file_exists(filename):
    return os.path.isfile('json/' + filename + '.json')


def create_file(filename, content):
    with open('json/' + filename + '.json', 'w') as q:
        json.dump(content, q, ensure_ascii=False, indent=4)