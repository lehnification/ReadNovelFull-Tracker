import os
import psycopg2
from psycopg2 import Error, sql




def get_setting(value):
    q = sql.SQL("SELECT {} from {} where {} =%s").format(sql.Identifier('value'), sql.Identifier('settings'), sql.Identifier('name'))
    return get_from_db(q, (value,))

def get_novels():
    q = sql.SQL("SELECT {} FROM {}").format(sql.SQL('*'), sql.Identifier('novels'))
    return get_from_db(q, None)
    
def get_from_db(query, data):
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        cursor.execute(query, data)
        if data is None:
            return cursor.fetchall()
        else: 
            return cursor.fetchone()[0]
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
        cursor.execute("UPDATE novels set last_chapter = %s, error = %s where novel = %s", (last_chapter, 0, novel))
        connection.commit()
        return cursor.rowcount == 1
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()

def mark_error(novel):
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        cursor.execute("UPDATE novels set error = %s where novel = %s", (1, novel))
        connection.commit()
        return cursor.rowcount == 1
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()