"""
This script will only be needed when removing files after already crawling them from the original corpus.
Specifically, after discarding some shorter articles (<15 paragraphs), we lose about 200 articles, which we purge
from the corresponding offline corpus with this script.
"""

from tqdm import tqdm

import json
import os

if __name__ == '__main__':
    with open("./data/articles.json") as f:
        articles = json.load(f)

    klexikon_folder = "./data/raw/klexikon/"
    wiki_folder = "./data/raw/wiki/"

    klexikon_articles = os.listdir(klexikon_folder)
    wiki_articles = os.listdir(wiki_folder)

    # Remove all files that *should* appear. The JSON file should only contain those
    # articles that should actually be taken into consideration.
    for article in tqdm(articles):
        article_title = f"{article['title'].replace(' ', '_').replace('/', '_')}.txt"

        klexikon_articles.remove(article_title)
        wiki_articles.remove(article_title)

    for article in klexikon_articles:
        os.remove(os.path.join(klexikon_folder, article))

    # This loop should be the same articles, but may contain some stragglers.
    for article in wiki_articles:
        os.remove(os.path.join(wiki_folder, article))

