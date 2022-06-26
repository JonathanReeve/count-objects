#!/usr/bin/env python3


import sqlite3
import os
import argparse
import logging

dataLocation = '/run/media/jon/Sekurkopioj/Corpora'
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

parser = argparse.ArgumentParser(
    description='Create a new text corpus out of Project Gutenberg texts..')
parser.add_argument('--dbPath', type=str,
                    help='Path to the database location')
parser.add_argument('--programPath', type=str,
                    help='Path to the program location')
args = parser.parse_args()

conn = sqlite3.connect(f"{dataLocation}/pg-text-7.db")
c = conn.cursor()

# Get only those books with Library of Congress Category "PR"
# (British Literature), and which are written in English.
# c.execute('select id from meta where LCC like "%PR%" and languages like "%en%";')
c.execute(
    """select id from meta
    where LCC like "%PR%"
    and languages like "%en%"
    and (
        gr_pubDate like "18%"
        or gr_pubDate like "189%"
        or gr_pubDate like "190%"
        or gr_pubDate like "191%"
        or gr_pubDate like "192%"
        or gr_pubDate like "193%"
        or wp_publication_date like "18%"
        or wp_publication_date like "191%"
        or wp_publication_date like "192%"
        or wp_publication_date like "193%"
    ) order by gr_pubDate;""")
idList = [item[0] for item in c.fetchall()]


def slugify(text):
    return "".join(x for x in text if x.isalnum())


def getResult(default):
    result = c.fetchone()
    if result is not None:
        return result[0]
    else:
        return default

for bookId in idList:
    bookIdSanitized = str(float(bookId))
    c.execute('SELECT text from text where id=?;', [bookId])
    text = getResult("")
    if text == "":
        continue  # Skip it if there's no text.
    c.execute('SELECT title from meta where id=?;', [bookIdSanitized])
    title = getResult(bookId)
    if len(title) > 50:
        title = title[:51]  # Truncate titles
    c.execute('SELECT gr_pubDate from meta where id=?;', [bookIdSanitized])
    pubDateGR = getResult(bookId)
    c.execute('SELECT wp_publication_date from meta where id=?;', [bookIdSanitized])
    pubDateWP = getResult(bookId)
    if len(pubDateGR) == 0 and len(pubDateWP) == 0:
        continue
    try:
        pubDate = str(min(int(pubDateGR[:4]), int(pubDateWP[:4])))
    except:
        pubDate = pubDateGR
    if len(pubDate) == 0:
        continue
    filename = f"{slugify(pubDate)}-{slugify(title)}-{bookIdSanitized}.txt"
    open(f'./pg-text4/{filename}', 'w').write(text)
    logging.info(f"Writing {filename}.")
