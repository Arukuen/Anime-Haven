import sqlite3
from datetime import datetime
from datetime import timedelta

class Anime:
    def __init__(self, title, image_url, anilist_id) -> None:
        self.title = title
        self.image_url = image_url
        self.anilist_id = anilist_id


class User:
    def __init__(self, username, discord_id) -> None:
        self.username = username
        self.discord_id = discord_id



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



def db_add_entry(date, rank, discord_id, anilist_id):
  conn = sqlite3.connect('data.db')
  c = conn.cursor()
  c.execute(f'SELECT UserId FROM User WHERE DiscordId = "{discord_id}"')
  user_id = c.fetchone()[0]
  c.execute(f'SELECT AnimeId FROM Anime WHERE AnilistId = "{anilist_id}"')
  anime_id = c.fetchone()[0]
  c.execute ('PRAGMA foreign_keys = ON')
  c.execute('INSERT INTO Entry VALUES (NULL,?,?,?,?)', (date, rank, user_id, anime_id))
  conn.commit()
  conn.close()
  return 0



# Can fetch user by only supplying either one of the two parameter
def db_get_user(username = False, discord_id = False):
  conn = sqlite3.connect('data.db')
  c = conn.cursor()
  if username and discord_id:
    c.execute(f'SELECT Username, DiscordId FROM User WHERE Username = "{username}" AND DiscordId = "{discord_id}"')
  else:
    if username:
      c.execute(f'SELECT Username, DiscordId FROM User WHERE Username = "{username}"')
    if discord_id:
      c.execute(f'SELECT Username, DiscordId FROM User WHERE DiscordId = "{discord_id}"')
  user = c.fetchone()
  conn.commit()
  conn.close()
  if user == None:
    return False
  else:
    return User(user[0], user[1])



def db_get_anime(anilist_id):
  conn = sqlite3.connect('data.db')
  c = conn.cursor()
  c.execute(f'SELECT Title, ImageUrl, AnilistId FROM Anime WHERE AnilistId = "{anilist_id}"')
  anime = c.fetchone()
  conn.commit()
  conn.close()
  if anime == None:
    return False
  else:
    return Anime(anime[0], anime[1], anime[2])



def db_is_user_match_anime(discord_id, anilist_id):
  conn = sqlite3.connect('data.db')
  c = conn.cursor()
  c.execute(f'SELECT UserId FROM User WHERE DiscordId = "{discord_id}"')
  user_id = c.fetchone()[0]
  c.execute(f'SELECT AnimeId FROM Anime WHERE AnilistId = "{anilist_id}"')
  anime_id = c.fetchone()[0]

  c.execute(f'SELECT * FROM Entry WHERE UserId = {user_id} And AnimeId = {anime_id}')
  anime = c.fetchone()
  conn.commit()
  conn.close()
  if anime == None:
    return False
  else:
    return True



def db_get_anime_list_by_user(discord_id):
  conn = sqlite3.connect('data.db')
  c = conn.cursor()
  c.execute(f'SELECT UserId FROM User WHERE DiscordId = "{discord_id}"')
  user_id = c.fetchone()[0]
  c.execute(f'''
    SELECT Anime.Title, Anime.ImageUrl, Anime.AnilistId
      FROM Entry JOIN Anime 
      ON Entry.AnimeId = Anime.AnimeId 
      WHERE Entry.UserId = {user_id}
  ''')
  anime_titles = c.fetchall()
  conn.commit()
  conn.close()
  if anime_titles == []:
    return False
  else:
    return list(map(lambda anime: Anime(anime[0], anime[1], anime[2]), anime_titles))



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