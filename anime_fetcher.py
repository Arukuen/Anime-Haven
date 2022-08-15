from Pymoe import Anilist
from database import Anime

instance = Anilist()

# Return an instance of Anime if successful, returns None if no anime is found with the term provided
def search_anime(term):
  data = instance.search.anime(term)['data']['Page']
  if data['pageInfo']['total'] >= 1:
    first_result = data['media'][0]
    # Some anime does not have english name, so fallback to romaji
    title = f'{first_result["title"]["romaji"]} ({first_result["title"]["english"]})' if first_result['title']['english'] != None else first_result['title']['romaji']
    image_url = first_result['coverImage']['large']
    anilist_id = first_result['id']
    return Anime(title, image_url, anilist_id)
  return None
