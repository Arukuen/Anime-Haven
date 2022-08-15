import database
import anime_fetcher
from datetime import datetime


# Returns an instance of Anime if successful, error message when failed
def add(username, discord_id, search_term, input_rank):
  if input_rank <= 0:
    return 'Invalid rank, use natural number'

  anime = anime_fetcher.search_anime(search_term)
  if not database.db_get_user(discord_id=discord_id):
    database.db_add_user(username, discord_id)
  if not database.db_get_anime(anime.anilist_id):
    database.db_add_anime(anime.title, anime.image_url, anime.anilist_id)

  date_string = datetime.now().strftime('%Y-%m-%d %H:%M:%S.000')
  anime_entries = database.db_get_anime_list_by_user(discord_id)
  
  # The user has previous animes in database
  if anime_entries:
    # The number of entry for a user is the also the highest rank
    max_rank = len(anime_entries)
  else:
    max_rank = 0
  
  if input_rank > max_rank:
    input_rank = max_rank + 1 
  else:
    database.db_preprocess_rank(discord_id, input_rank)

  if database.db_is_user_match_anime(discord_id, anime.anilist_id):
    return 'Anime already exists for the user'
  database.db_add_entry(date_string, input_rank, discord_id, anime.anilist_id)
  return anime



# Returns a list of instance of anime if successful, error message when failed
def userlist(username):
  user = database.db_get_user(username=username)
  if not user:
    return 'User does not exist'
  anime_titles = database.db_get_anime_list_by_user(user.discord_id)
  if not anime_titles:
    return 'Empty anime list by user'
  return anime_titles

