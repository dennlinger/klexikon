"""
Dummy script to speed up evaluation process
"""

from tqdm import tqdm
import pickle

import numpy as np

from .compare_offline_corpus import get_unique_lemmas, get_nouns_verbs_adjectives_adverbs_only
from .utils import directory_iterator


if __name__ == "__main__":

    wiki_vocab = set()
    klexikon_vocab = set()

    wiki_per_doc_vocab_size = []
    klexikon_per_doc_vocab_size = []

    wiki_tokens = []
    klexikon_tokens = []

    counter = 0
    for wiki_fp, klexikon_fp in tqdm(directory_iterator("./data/raw/wiki", "./data/raw/klexikon")):
        counter += 1
        if counter >= 100:
            break

        with open(wiki_fp) as f:
            wiki_article = tuple(f.readlines())
        with open(klexikon_fp) as f:
            klexikon_article = tuple(f.readlines())

            wiki_doc_vocab = get_unique_lemmas(wiki_article)
            klexikon_doc_vocab = get_unique_lemmas(klexikon_article)

            wiki_vocab = wiki_vocab.union(wiki_doc_vocab)
            klexikon_vocab = klexikon_vocab.union(klexikon_doc_vocab)

            wiki_per_doc_vocab_size.append(len(wiki_doc_vocab))
            klexikon_per_doc_vocab_size.append(len(klexikon_doc_vocab))

            wiki_tokens.extend(get_nouns_verbs_adjectives_adverbs_only(wiki_article))
            klexikon_tokens.extend(get_nouns_verbs_adjectives_adverbs_only(klexikon_article))

    # Vocabulary stats
    print(f"Wikipedia total distinct tokens: {len(wiki_vocab)}")
    print(f"Klexikon total distinct tokens:  {len(klexikon_vocab)}")

    print(f"Wikipedia vocab size per doc: {np.mean(wiki_per_doc_vocab_size):.2f} +/- {np.std(wiki_per_doc_vocab_size):.2f}")
    print(f"Klexikon vocab size per doc:  {np.mean(klexikon_per_doc_vocab_size):.2f} +/- {np.std(klexikon_per_doc_vocab_size):.2f}")

    wiki_token_lengths = [len(token) for token in wiki_tokens]
    klexikon_token_lengths = [len(token) for token in klexikon_tokens]
    print(f"Wikipedia average token length per noun/verb/adj/adv: {np.mean(wiki_token_lengths):.2f} +/- "
          f"{np.std(wiki_token_lengths):.2f}")
    print(f"Klexikon average token length per noun/verb/adj/adv:  {np.mean(klexikon_token_lengths):.2f} +/- "
          f"{np.std(klexikon_token_lengths):.2f}")

    with open("wiki_tokens.pkl", "wb") as f:
        pickle.dump(wiki_tokens, f)

    with open("klexikon_tokens.pkl", "wb") as f:
        pickle.dump(klexikon_tokens, f)