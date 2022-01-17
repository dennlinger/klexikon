"""
Dummy script to speed up evaluation process
"""

from collections import Counter
from tqdm import tqdm
import pickle

import spacy

from .utils import directory_iterator


if __name__ == "__main__":

    wiki_vocab = set()
    klexikon_vocab = set()

    wiki_per_doc_vocab_size = []
    klexikon_per_doc_vocab_size = []

    wiki_lemmas = []
    klexikon_lemmas = []

    wiki_articles = []
    klexikon_articles = []

    counter = 0
    for wiki_fp, klexikon_fp in tqdm(directory_iterator("./data/raw/wiki", "./data/raw/klexikon")):
        counter += 1
        # if counter >= 50:
        #     break

        with open(wiki_fp) as f:
            wiki_articles.append("".join(f.readlines()).replace("\n", " "))
        with open(klexikon_fp) as f:
            klexikon_articles.append("".join(f.readlines()).replace("\n", " "))

    nlp = spacy.load("de_core_news_md", disable=("ner"))

    for wiki_text, klexikon_text in tqdm(zip(wiki_articles, klexikon_articles)):
        wiki_lemmas.extend([token.lemma_ for token in nlp(wiki_text)])
        klexikon_lemmas.extend([token.lemma_ for token in nlp(klexikon_text)])

    wiki_counter = Counter(wiki_lemmas)
    klexikon_counter = Counter(klexikon_lemmas)

    wiki_sum_top_1000 = sum([frequency for lemma, frequency in wiki_counter.most_common(1000)])
    klexikon_sum_top_1000 = sum([frequency for lemma, frequency in klexikon_counter.most_common(1000)])
    print(f"Share of top 1000 words for Wikipedia: {wiki_sum_top_1000 / len(wiki_lemmas) * 100:.2f}")
    print(f"Share of top 1000 words for Klexikon:  {klexikon_sum_top_1000 / len(klexikon_lemmas) * 100:.2f}")

    with open("wiki_lemmas.pkl", "wb") as f:
        pickle.dump(wiki_lemmas, f)

    with open("klexikon_lemmas.pkl", "wb") as f:
        pickle.dump(klexikon_lemmas, f)