import database
import anime_fetcher
from datetime import datetime


# Returns an instance of Anime if successful, error message when failed
def add_anime(username, discord_id, search_term, input_rank):
  if input_rank <= 0:
    return 'Invalid rank, use positive number'
  anime = anime_fetcher.search_anime(search_term)
  if not database.db_get_user(discord_id=discord_id):
    database.db_add_user(username, discord_id)
  if not database.db_get_anime(anime.anilist_id):
    database.db_add_anime(anime.title, anime.image_url, anime.anilist_id)
  # Exit here if anime already exists to user
  if database.db_is_user_match_anime(discord_id, anime.anilist_id):
    return 'Anime already exists for the user'

  date_string = datetime.now().strftime('%Y-%m-%d %H:%M:%S.000')
  anime_entries = database.db_get_anime_list_by_user(discord_id)
  # The user has previous animes in database
  # The number of entry for a user is the also the highest rank
  max_rank = len(anime_entries) if anime_entries else 0
  if input_rank > max_rank:
    input_rank = max_rank + 1 
  else:
    database.db_preprocess_anime_rank(discord_id, input_rank)
  database.db_add_anime_entry(date_string, input_rank, discord_id, anime.anilist_id)
  return anime, input_rank



def add_character(username, discord_id, search_term, input_rank):
  if input_rank <= 0:
    return 'Invalid rank, use positive number'
  character = anime_fetcher.search_character(search_term)
  if not database.db_get_user(discord_id=discord_id):
    database.db_add_user(username, discord_id)
  if not database.db_get_character(character.anilist_id):
    database.db_add_character(character.name, character.image_url, character.anilist_id)
  # Exit here if character already exists to user
  if database.db_is_user_match_character(discord_id, character.anilist_id):
    return 'Character already exists for the user'

  date_string = datetime.now().strftime('%Y-%m-%d %H:%M:%S.000')
  character_entries = database.db_get_character_list_by_user(discord_id)
  # The user has previous character in database
  # The number of entry for a user is the also the highest rank
  max_rank = len(character_entries) if character_entries else 0
  if input_rank > max_rank:
    input_rank = max_rank + 1 
  else:
    database.db_preprocess_character_rank(discord_id, input_rank)
  database.db_add_character_entry(date_string, input_rank, discord_id,character.anilist_id)
  return character, input_rank


# Returns a list of instance of anime if successful, error message when failed
def list_anime(username):
  user = database.db_get_user(username=username)
  if not user:
    return 'User does not exist'
  anime_titles = database.db_get_anime_list_by_user(user.discord_id)
  if not anime_titles:
    return 'Empty anime list by user'
  return anime_titles


def list_character(username):
  user = database.db_get_user(username=username)
  if not user:
    return 'User does not exist'
  character_titles = database.db_get_character_list_by_user(user.discord_id)
  if not character_titles:
    return 'Empty character list by user'
  return character_titles
