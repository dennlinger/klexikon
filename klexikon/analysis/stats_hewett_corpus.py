"""
Script to compute the average number of sentences for the Hewett and Stede version of a Klexikon dataset.
For this to work, the lexica-corpus github repository (https://github.com/fhewett/lexica-corpus)
is expected to reside in the same parent folder as the klexikon repository.
"""
import json
import spacy

import numpy as np
from tqdm import tqdm


if __name__ == '__main__':
    with open("../../../lexica-corpus/wiki_corpus.txt") as f:
        wiki_data = json.load(f)["wiki"]
    with open("../../../lexica-corpus/klexi_corpus.txt") as f:
        klexikon_data = json.load(f)["klexikon"]

    nlp = spacy.load("de_core_news_md", disable=("ner"))

    wiki_stats = []
    for article in tqdm(wiki_data):
        article_text = article["text"].replace("<eop>", " ")
        wiki_stats.append(len(list(nlp(article_text).sents)))

    klexikon_stats = []
    for article in tqdm(klexikon_data):
        article_text = article["text"].replace("<eop>", " ")
        klexikon_stats.append(len(list(nlp(article_text).sents)))

    print(f"Stats for the Klexikon corpus (only simplification level 1) by Hewett and Stede:")
    print(f"Average number of sentences for Wikipedia: {np.mean(wiki_stats):.2f}")
    print(f"Average number of sentences for Klexikon:  {np.mean(klexikon_stats):.2f}")
    print(f"Median number of sentences for Wikipedia: {np.median(wiki_stats):.2f}")
    print(f"Median number of sentences for Klexikon:  {np.median(klexikon_stats):.2f}")

    print(f"Standard deviation Wikipedia: {np.std(wiki_stats):.2f}")
    print(f"Standard deviation for Klexikon:  {np.std(klexikon_stats):.2f}")