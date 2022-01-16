"""
Check for what amount of topics there exists a corresponding article in German Wikipedia with the exact same heading
"""

from utils import get_klexikon_titles
from time import sleep
from tqdm import tqdm
import requests


def check_german_wikipedia(title: str) -> bool:
    """
    Checks whether a page with the exact same title exists on German Wikipedia.
    :param title:
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
    print(len(res.json()['query']['search']))
    for search_result in res.json()['query']['search']:
        if search_result['title'] == title:
            return True
    return False


if __name__ == "__main__":
    fn = "./data/article_urls.txt"
    titles = get_klexikon_titles(fn)
    contained = [False] * len(titles)
    for idx, title in enumerate(tqdm(titles)):
        contained[idx] = check_german_wikipedia(title)
        # Wikipedia is generally very strict about rate limiting, so do this carefully.
        sleep(0.05)

    print(f"{sum(contained) / len(contained) * 100:.2f}% of articles are on Wikipedia.")
    print(f"{len(contained) - sum(contained)} articles are missing. These are:")
    for contain_bool, title in zip(contained, titles):
        if not contain_bool:
            print(title)


