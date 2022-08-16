from pprint import pprint
from Pymoe import Anilist
from database import Anime
from database import Character

anilist = Anilist()

# Return an anilist of Anime if successful, returns None if no anime is found with the term provided
def search_anime(term):
  data = anilist.search.anime(term)['data']['Page']
  if data['pageInfo']['total'] >= 1:
    first_result = data['media'][0]
    # Some anime does not have english name, so fallback to romaji
    title = f'{first_result["title"]["romaji"]} ({first_result["title"]["english"]})' if first_result['title']['english'] != None else first_result['title']['romaji']
    image_url = first_result['coverImage']['large']
    anilist_id = first_result['id']
    return Anime(title, image_url, anilist_id)
  return None


def search_character(term):
  data = anilist.search.character(term)['data']['Page']
  if data['pageInfo']['total'] >= 1:
    first_result = data['characters'][0]
    # Some chracters does not have last name, so fallback to just first name
    name = f'{first_result["name"]["last"]} {first_result["name"]["first"]}' if first_result['name']['last'] != None else first_result['name']['first']
    image_url = first_result['image']['large']
    anilist_id = first_result['id']
    return Character(name, image_url, anilist_id)
  return None