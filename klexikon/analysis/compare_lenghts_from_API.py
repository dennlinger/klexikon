"""
Utilize the return parameters from Klexikon to determine the word count of an article.
There is also a different script calculating the number of sentences based on our own split,
which can be found in the same folder.
Note that this is merely an approximation, since we rely on the title being the same for both the Wikipedia and
Klexikon articles, which several steps in our preprocessing indicate is an incorrect assumption. In addition to that,
some of our preprocessing steps potentially discard text (e.g., figure descriptions or lists), which falsifies these
results even further.
"""

from .utils import get_klexikon_titles
from time import sleep
from tqdm import tqdm
import numpy as np
import requests


def get_word_count(title, base_url="https://klexikon.zum.de/api.php") -> int:
    """
    Return the word count of an Klexikon article.
    :param title:
    :param base_url
    :return:
    """
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srlimit": 5,
        "srsearch": title
    }
    try:
        res = requests.get(url=base_url, params=params)
        # print(len(res.json()['query']['search']))
        article = res.json()['query']['search'][0]
        return article['wordcount']
    except IndexError:  # Likely due to incorrect search results.
        return 0


def stats(word_counts, source="Klexikon"):
    print(f"Statistics for {source} word counts:")
    print(f"Average number of words per article: {np.mean(word_counts)}")
    print(f"Maximum number of words: {max(word_counts)}")
    print(f"Minimum number of words: {min(word_counts)}")
    print(f"------------------------------------")


if __name__ == "__main__":
    fn = "./data/article_urls.txt"
    titles = get_klexikon_titles(fn)
    klexikon_word_counts = []
    wiki_word_counts = []
    for title in tqdm(titles):
        klexikon_word_counts.append(get_word_count(title, base_url="https://klexikon.zum.de/api.php"))
        wiki_word_counts.append(get_word_count(title, base_url="https://de.wikipedia.org/w/api.php"))
        sleep(0.05)
