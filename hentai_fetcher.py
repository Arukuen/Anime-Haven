from hentai import Utils, Sort, Option, Tag, Format
from pathlib import Path
import random

def random_hentai():
    item = Utils.get_random_hentai()
    img_url = random.choice(item.image_urls)
    title = item.title(Format.Pretty)
    return (title, img_url)
