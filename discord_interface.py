import database
import anime_fetcher


# Returns an instance of Anime if successful, error message when failed
def add(username, discord_id, search_term, rank):
  anime = anime_fetcher.search_anime(search_term)
  if not database.db_get_user(discord_id=discord_id):
    database.db_add_user(username, discord_id)
  if not database.db_get_anime(anime.anilist_id):
    database.db_add_anime(anime.title, anime.image_url, anime.anilist_id)
  if database.db_is_user_match_anime(discord_id, anime.anilist_id):
    return 'Anime already exists for the user'
  database.db_add_entry('11-08-2022 11:11:00.000', rank, discord_id, anime.anilist_id)
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

