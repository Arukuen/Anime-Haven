from Pymoe import Anilist
import pprint

instance = Anilist()

def search_anime(term):
    data = instance.search.anime(term)['data']['Page']
    #pprint.pprint(data)
    if data['pageInfo']['total'] >= 1:
        first_result = data['media'][0]

        if first_result['title']['english'] != None:
            first_title = f'{first_result["title"]["romaji"]} ({first_result["title"]["english"]})'
        else:
            first_title = first_result['title']['romaji']

        first_image = first_result['coverImage']['large']
        return (first_title, first_image)

    return None


    
""" for y in range(len(x['data']['Page']['media'])):
    print(x['data']['Page']['media'][y]['title']['english']) """
