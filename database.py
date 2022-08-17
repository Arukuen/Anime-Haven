import sqlite3
from datetime import datetime
from datetime import timedelta

class User:
  def __init__(self, username, discord_id) -> None:
    self.username = username
    self.discord_id = discord_id


class Anime:
  def __init__(self, title, image_url, anilist_id) -> None:
    self.title = title
    self.image_url = image_url
    self.anilist_id = anilist_id


class Character:
  def __init__(self, name, image_url, anilist_id) -> None:
    self.name = name
    self.image_url = image_url
    self.anilist_id = anilist_id


class AnimeEntry:
  def __init__(self, title, image_url, anilist_id, date, rank) -> None:
    self.title = title
    self.image_url = image_url
    self.anilist_id = anilist_id
    self.date = date
    self.rank = rank


class CharacterEntry:
  def __init__(self, name, image_url, anilist_id, date, rank) -> None:
    self.name = name
    self.image_url = image_url
    self.anilist_id = anilist_id
    self.date = date
    self.rank = rank




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
      CREATE TABLE Character (
        CharacterId   INTEGER   PRIMARY KEY,
        Name          TEXT      NOT NULL,
        ImageUrl      TEXT      NOT NULL,
        AnilistId     INTEGER   NOT NULL
      )
    ''')
    c.execute('''
      CREATE TABLE AnimeEntry (
        EntryId   INTEGER   PRIMARY KEY,
        Date      TEXT      NOT NULL,
        Rank      INTEGER   NOT NULL,
        UserId    INTEGER   NOT NULL,
        AnimeId   INTEGER   NOT NULL,
        FOREIGN KEY(UserId) REFERENCES User(UserId),
        FOREIGN KEY(AnimeId) REFERENCES Anime(AnimeId)
      )
    ''')
    c.execute('''
      CREATE TABLE CharacterEntry (
        EntryId       INTEGER   PRIMARY KEY,
        Date          TEXT      NOT NULL,
        Rank          INTEGER   NOT NULL,
        UserId        INTEGER   NOT NULL,
        CharacterId   INTEGER   NOT NULL,
        FOREIGN KEY(UserId) REFERENCES User(UserId),
        FOREIGN KEY(CharacterId) REFERENCES Character(CharacterId)
      )
    ''')
    conn.commit()
    conn.close()
    return 0



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



def db_add_character(name, image_url, anilist_id):
  conn = sqlite3.connect('data.db')
  c = conn.cursor()
  c.execute('INSERT INTO Character VALUES (NULL,?,?,?)', (name, image_url, anilist_id))
  conn.commit()
  conn.close()
  return 0



def db_add_anime_entry(date, rank, discord_id, anilist_id):
  conn = sqlite3.connect('data.db')
  c = conn.cursor()
  c.execute(f'SELECT UserId FROM User WHERE DiscordId = "{discord_id}"')
  user_id = c.fetchone()[0]
  c.execute(f'SELECT AnimeId FROM Anime WHERE AnilistId = "{anilist_id}"')
  anime_id = c.fetchone()[0]
  c.execute ('PRAGMA foreign_keys = ON')
  c.execute('INSERT INTO AnimeEntry VALUES (NULL,?,?,?,?)', (date, rank, user_id, anime_id))
  conn.commit()
  conn.close()
  return 0



def db_add_character_entry(date, rank, discord_id, anilist_id):
  conn = sqlite3.connect('data.db')
  c = conn.cursor()
  c.execute(f'SELECT UserId FROM User WHERE DiscordId = "{discord_id}"')
  user_id = c.fetchone()[0]
  c.execute(f'SELECT CharacterId FROM Character WHERE AnilistId = "{anilist_id}"')
  character_id = c.fetchone()[0]
  c.execute ('PRAGMA foreign_keys = ON')
  c.execute('INSERT INTO CharacterEntry VALUES (NULL,?,?,?,?)', (date, rank, user_id, character_id))
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



def db_get_character(anilist_id):
  conn = sqlite3.connect('data.db')
  c = conn.cursor()
  c.execute(f'SELECT Name, ImageUrl, AnilistId FROM Character WHERE AnilistId = "{anilist_id}"')
  character = c.fetchone()
  conn.commit()
  conn.close()
  if character == None:
    return False
  else:
    return Character(character[0], character[1], character[2])



def db_is_user_match_anime(discord_id, anilist_id):
  conn = sqlite3.connect('data.db')
  c = conn.cursor()
  c.execute(f'SELECT UserId FROM User WHERE DiscordId = "{discord_id}"')
  user_id = c.fetchone()[0]
  c.execute(f'SELECT AnimeId FROM Anime WHERE AnilistId = "{anilist_id}"')
  anime_id = c.fetchone()[0]

  c.execute(f'SELECT * FROM AnimeEntry WHERE UserId = {user_id} And AnimeId = {anime_id}')
  anime = c.fetchone()
  conn.commit()
  conn.close()
  if anime == None:
    return False
  else:
    return True



def db_is_user_match_character(discord_id, anilist_id):
  conn = sqlite3.connect('data.db')
  c = conn.cursor()
  c.execute(f'SELECT UserId FROM User WHERE DiscordId = "{discord_id}"')
  user_id = c.fetchone()[0]
  c.execute(f'SELECT CharacterId FROM Character WHERE AnilistId = "{anilist_id}"')
  anime_id = c.fetchone()[0]

  c.execute(f'SELECT * FROM CharacterEntry WHERE UserId = {user_id} And CharacterId = {anime_id}')
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
    SELECT 
      Anime.Title,
      Anime.ImageUrl,
      Anime.AnilistId,
      AnimeEntry.Date,
      AnimeEntry.Rank
    FROM
      AnimeEntry 
    JOIN Anime 
      ON AnimeEntry.AnimeId = Anime.AnimeId
    WHERE 
      AnimeEntry.UserId = {user_id}
    ORDER BY
      AnimeEntry.Rank ASC
  ''')
  entries = c.fetchall()
  conn.commit()
  conn.close()
  if entries == []:
    return False
  else:
    return list(map(lambda entry: AnimeEntry(entry[0], entry[1], entry[2], entry[3], entry[4]), entries))



def db_get_character_list_by_user(discord_id):
  conn = sqlite3.connect('data.db')
  c = conn.cursor()
  c.execute(f'SELECT UserId FROM User WHERE DiscordId = "{discord_id}"')
  user_id = c.fetchone()[0]
  c.execute(f'''
    SELECT 
      Character.Name,
      Character.ImageUrl,
      Character.AnilistId,
      CharacterEntry.Date,
      CharacterEntry.Rank
    FROM
      CharacterEntry 
    JOIN Character 
      ON CharacterEntry.CharacterId = Character.CharacterId
    WHERE 
      CharacterEntry.UserId = {user_id}
    ORDER BY
      CharacterEntry.Rank ASC
  ''')
  entries = c.fetchall()
  conn.commit()
  conn.close()
  if entries == []:
    return False
  else:
    return list(map(lambda entry: CharacterEntry(entry[0], entry[1], entry[2], entry[3], entry[4]), entries))



def db_preprocess_anime_rank(discord_id, input_rank):
  conn = sqlite3.connect('data.db')
  c = conn.cursor()
  c.execute(f'SELECT UserId FROM User WHERE DiscordId = "{discord_id}"')
  user_id = c.fetchone()[0]
  c.execute(f'SELECT COUNT(EntryId) From AnimeEntry WHERE UserId = {user_id}')
  max_rank = c.fetchone()[0]
  # Reverse to resolve double operation
  for current_rank in range(max_rank, input_rank-1, -1):
    c.execute(f'UPDATE AnimeEntry SET Rank = {current_rank + 1} WHERE Rank = {current_rank}')
  conn.commit()
  conn.close()
  return 0



def db_preprocess_character_rank(discord_id, input_rank):
  conn = sqlite3.connect('data.db')
  c = conn.cursor()
  c.execute(f'SELECT UserId FROM User WHERE DiscordId = "{discord_id}"')
  user_id = c.fetchone()[0]
  c.execute(f'SELECT COUNT(EntryId) From CharacterEntry WHERE UserId = {user_id}')
  max_rank = c.fetchone()[0]
  # Reverse to resolve double operation
  for current_rank in range(max_rank, input_rank-1, -1):
    c.execute(f'UPDATE CharacterEntry SET Rank = {current_rank + 1} WHERE Rank = {current_rank}')
  conn.commit()
  conn.close()
  return 0



# For test only, will delete
def db_reset():
  conn = sqlite3.connect('data.db')
  c = conn.cursor()
  c.execute('DROP TABLE User')
  c.execute('DROP TABLE Anime')
  c.execute('DROP TABLE Character')
  c.execute('DROP TABLE AnimeEntry')
  c.execute('DROP TABLE CharacterEntry')
  conn.commit()
  conn.close()
  return 0