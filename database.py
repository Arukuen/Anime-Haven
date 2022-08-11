# TODO:
# Handle duplicate in adding in database

from dis import disco
import sqlite3
from datetime import datetime
from datetime import timedelta


def db_create_tables():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
      CREATE TABLE User (
        UserId    INTEGER   PRIMARY KEY,
        Username  TEXT      NOT NULL,
        DiscordId INTEGER   NOT NULL
      )
    ''')
    
    c.execute('''
      CREATE TABLE Anime (
        AnimeId   INTEGER   PRIMARY KEY,
        Title     TEXT      NOT NULL,
        ImageUrl  TEXT      NOT NULL,
        AnilistId INTEGER   NOT NULL
      )
    ''')

    c.execute('''
      CREATE TABLE Entry (
        EntryId        INTEGER   PRIMARY KEY,
        Date      TEXT      NOT NULL,
        Rank      INTEGER   NOT NULL,
        UserId    INTEGER   NOT NULL,
        AnimeId   INTEGER   NOT NULL,
        FOREIGN KEY(UserId) REFERENCES User(UserId),
        FOREIGN KEY(AnimeId) REFERENCES Anime(AnimeId)
      )
    ''')
    conn.commit()
    conn.close()
    return 0


def db_fetch_table(table_name, column = '*', condition = False):
  conn = sqlite3.connect('data.db')
  c = conn.cursor()
  if condition:
    c.execute(f'SELECT {column} FROM {table_name} WHERE {condition}')
  else: 
    c.execute(f'SELECT {column} FROM {table_name}')
  items = c.fetchall()
  conn.commit()
  conn.close()
  return items



def db_add_user(username, discord_id):
  conn = sqlite3.connect('data.db')
  c = conn.cursor()
  c.execute('INSERT INTO User VALUES (NULL,?,?)', (username, discord_id))
  conn.commit()
  conn.close()
  return 0


def db_add_anime(title, image_url, anilist_id):
  conn = sqlite3.connect('data.db')
  c = conn.cursor()
  c.execute('INSERT INTO Anime VALUES (NULL,?,?,?)', (title, image_url, anilist_id))
  conn.commit()
  conn.close()
  return 0


def db_add_entry(date, rank, user_id, anime_id):
  conn = sqlite3.connect('data.db')
  c = conn.cursor()
  c.execute ('PRAGMA foreign_keys = ON')
  c.execute('INSERT INTO Entry VALUES (NULL,?,?,?,?)', (date, rank, user_id, anime_id))
  conn.commit()
  conn.close()
  return 0


def db_get_user(discord_id, column = '*'):
  conn = sqlite3.connect('data.db')
  c = conn.cursor()
  c.execute(f'SELECT {column} FROM User WHERE DiscordId = "{discord_id}"')
  user = c.fetchone()
  conn.commit()
  conn.close()
  print(user)
  if user == None:
    return False
  else:
    return user


def db_get_anime(anilist_id, column = '*'):
  conn = sqlite3.connect('data.db')
  c = conn.cursor()
  c.execute(f'SELECT {column} FROM Anime WHERE AnilistId = "{anilist_id}"')
  anime = c.fetchone()
  conn.commit()
  conn.close()
  if anime == None:
    return False
  else:
    return anime



# For test only, will delete
def db_reset():
  conn = sqlite3.connect('data.db')
  c = conn.cursor()
  c.execute('DROP TABLE User')
  c.execute('DROP TABLE Anime')
  c.execute('DROP TABLE Entry')
  conn.commit()
  conn.close()
  return 0


########### FOR TESTING ############
# db_reset()
# db_create_tables()

# db_add_user('Arukuen', 1234)
# db_add_anime('Arifureta', 'image.png', 4321)
# db_add_entry('11-08-2022 11:11:00.000', 100, 1, 1)