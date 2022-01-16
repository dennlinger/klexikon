"""
Create a final file with aligned URLs for Wikipedia and Klexikon.
"""

from ..analysis.utils import get_klexikon_titles, get_klexikon_urls
from tqdm import tqdm
import requests
import json
import os


def get_matching_wikipedia_url(title: str) -> str:
    """
    Automatically searches for a matching URL on German Wikipedia.
    If not matching article exists, present the user with options to choose from.
    :param title: Search term, equivalent to the Klexikon page title
    :return:
    """
    base_url = "https://de.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srlimit": 5,
        "srsearch": title
    }

    res = requests.get(url=base_url, params=params)
    data = res.json()
    for search_result in data['query']['search']:
        # If we find an exact match, take that article
        if search_result['title'] == title:
            return get_page_url_by_title(title, base_url)
    # If no exact match was found, manually disambiguate
    else:
        related_titles = [search_result['title'] for search_result in data['query']['search']]
        print(f"\nOriginal title of the Klexikon article: {title}")
        print([f"{idx}: {title}" for idx, title in enumerate(related_titles)])
        print("Enter the number of the most likely corresponding article. If none match, "
              "enter the exact wiki page title of the closest match.")
        user_input = input("Number / Title: ")
        try:
            user_input = int(user_input)

            return get_page_url_by_title(related_titles[user_input], base_url)
        except ValueError:
            return get_page_url_by_title(user_input, base_url)


def get_page_url_by_title(title: str, base_url: str) -> str:
    """
    Gets the full URL of a page associated with a specific title from Wikipedia API
    :param title: Title heading
    :param base_url: Wikipedia base URL
    :return: Full URL
    """
    params = {
        "action": "query",
        "format": "json",
        "prop": "info",
        "inprop": "url",
        "titles": title
    }

    res = requests.get(url=base_url, params=params)
    data = res.json()

    (page_id, entry), = data['query']['pages'].items()
    return entry['fullurl']


if __name__ == "__main__":
    fn = "./data/article_urls.txt"
    out_fn = "./data/articles.json"
    urls = get_klexikon_urls(fn)
    titles = get_klexikon_titles(fn)

    matching_urls = []

    if os.path.exists(out_fn):
        with open(out_fn, "r") as f:
            matching_urls = json.load(f)

    already_tagged = len(matching_urls)

    if len(urls) != len(titles):
        raise IndexError("Length of titles and Klexikon URLs not matching!")
    try:
        for idx, title in enumerate(tqdm(titles[already_tagged:]), start=already_tagged):
            curr_article = {"title": title,
                            "klexikon_url": urls[idx],
                            "wiki_url": get_matching_wikipedia_url(title)}

            matching_urls.append(curr_article)
    except:
        pass
    finally:
        with open(out_fn, "w") as f:
            json.dump(matching_urls, f, indent=2)
