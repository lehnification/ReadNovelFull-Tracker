import os
import psycopg2
from psycopg2 import Error




def get_setting(value):
    return get_from_db('value', 'settings', 'name', value)

def get_novels():
    return get_from_db('*', 'novels', None, None)
    
def get_from_db(select, table, where, value):
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        query = None
        data = None
        if where is None:
            query = "SELECT %s FROM %s"
            data = (select, table)
        else:
            query = "SELECT %s from %s where %s =%s"
            data = (select, table, where, value)
        cursor.execute(query, data)
        if where is None:
            return cursor.fetchall()
        else: return cursor.fetchone()[0]
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()

def insert_novel_initialisation(novel, name, id, last_chapter):
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        cursor.execute("UPDATE novels set name = %s, id = %s, last_chapter = %s where novel = %s", (name, id, last_chapter, novel))
        connection.commit()
        return cursor.rowcount == 1
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()

def update_last_chapter(last_chapter, novel):
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        cursor.execute("UPDATE novels set last_chapter = %s where novel = %s", (last_chapter, novel))
        connection.commit()
        return cursor.rowcount == 1
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()