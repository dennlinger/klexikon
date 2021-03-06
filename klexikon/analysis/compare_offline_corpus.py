"""
Using the available processed corpora, we can also compute basic statistics on the offline corpus.
"""

from functools import lru_cache
from typing import List, Set, Tuple
from tqdm import tqdm

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import spacy
from spacy.tokens.doc import Doc

from .utils import directory_iterator


def calculate_number_of_valid_lines(lines: Tuple[str]) -> int:
    """
    Note that this function does not count empty lines and headings.
    :param lines: Result of a f.readlines() operation, i.e., a list of strings.
    :return: The number of valid lines in this file
    """
    line_counter = 0
    for line in lines:
        if line.strip("\n ") and not line.startswith("=="):
            line_counter += 1
    return line_counter


def count_number_tokens(lines: Tuple[str]) -> int:
    """
    Counts the number of valid tokens by running a spacy model over the text.
    :param lines: Input text, in the form of lines in a list.
    :return: Counted number of tokens, as per the spacy tokenizer.
    """
    return len(process_text_with_spacy(lines))


def get_unique_lemmas(lines: Tuple[str]) -> Set:
    """
    Returns the unique tokens within a single document.
    """
    doc = process_text_with_spacy(lines)
    vocab = set([token.lemma_ for token in doc])
    return vocab


def get_nouns_verbs_adjectives_adverbs_only(lines: Tuple[str]) -> List[str]:
    relevant_words = []
    doc = process_text_with_spacy(lines)

    considered_pos_tags = {"NOUN", "ADV", "ADJ", "VERB"}
    for token in doc:
        if token.pos_ in considered_pos_tags:
            relevant_words.append(token.text.lower())

    return relevant_words


@lru_cache(maxsize=8)
def process_text_with_spacy(lines: Tuple[str]) -> Doc:

    text = "".join(lines).replace("\n", " ")
    nlp = get_spacy(disable=("ner"))

    return nlp(text)


@lru_cache(maxsize=2)
def get_spacy(model_name="de_core_news_md",
              disable=("ner", "tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer")
              ):
    """
    Per default only loads the tokenizer component
    """
    return spacy.load(model_name, disable=disable)


def print_stats(wiki_stats: List[int], klexikon_stats: List[int], unit: str = "sentences") -> None:
    """
    :param wiki_stats:
    :param klexikon_stats:
    :param unit:
    :return:
    """

    # TODO: Compute Confidence Intervals
    print(f"Average number of {unit} for Wikipedia: {np.mean(wiki_stats):.2f}")
    print(f"Average number of {unit} for Klexikon:  {np.mean(klexikon_stats):.2f}")
    print(f"Median number of {unit} for Wikipedia: {np.median(wiki_stats):.2f}")
    print(f"Median number of {unit} for Klexikon:  {np.median(klexikon_stats):.2f}")

    print(f"Standard deviation Wikipedia: {np.std(wiki_stats):.2f}")
    print(f"Standard deviation for Klexikon:  {np.std(klexikon_stats):.2f}")

    ratios = [wiki_value / klexikon_value for wiki_value, klexikon_value in zip(wiki_stats, klexikon_stats)]
    print(f"Global average ratio between {unit} of Wikipedia / Klexikon:       "
          f"{np.mean(wiki_stats) / np.mean(klexikon_stats):.2f}")
    print(f"Per-document average ratio between {unit} of Wikipedia / Klexikon: {np.mean(ratios):.2f}")

    plt.scatter(wiki_stats, klexikon_stats, marker=".")
    plt.savefig(f"./results/length_comparison_{unit}.png")
    plt.close()
    plt.scatter(wiki_stats, ratios, marker=".")
    plt.savefig(f"./results/wiki_length_vs_ratio_{unit}.png")
    plt.close()


if __name__ == "__main__":
    wiki_number_sentences = []
    klexikon_number_sentences = []

    wiki_number_tokens = []
    klexikon_number_tokens = []

    wiki_vocab = set()
    klexikon_vocab = set()

    wiki_per_doc_vocab_size = []
    klexikon_per_doc_vocab_size = []

    wiki_tokens = []
    klexikon_tokens = []

    for wiki_fp, klexikon_fp in tqdm(directory_iterator("./data/raw/wiki", "./data/raw/klexikon")):
        with open(wiki_fp) as f:
            wiki_article = tuple(f.readlines())
        with open(klexikon_fp) as f:
            klexikon_article = tuple(f.readlines())

            # Since lines equal sentences after preprocessing, we can simply count lines
            wiki_number_sentences.append(calculate_number_of_valid_lines(wiki_article))
            klexikon_number_sentences.append(calculate_number_of_valid_lines(klexikon_article))

            # Same for the tokens, only needed for sentence length calculation
            wiki_number_tokens.append(count_number_tokens(wiki_article))
            klexikon_number_tokens.append(count_number_tokens(klexikon_article))

            # Also count the number of unique words
            wiki_doc_vocab = get_unique_lemmas(wiki_article)
            klexikon_doc_vocab = get_unique_lemmas(klexikon_article)

            wiki_vocab = wiki_vocab.union(wiki_doc_vocab)
            klexikon_vocab = klexikon_vocab.union(klexikon_doc_vocab)

            wiki_per_doc_vocab_size.append(len(wiki_doc_vocab))
            klexikon_per_doc_vocab_size.append(len(klexikon_doc_vocab))

            wiki_tokens.extend(get_nouns_verbs_adjectives_adverbs_only(wiki_article))
            klexikon_tokens.extend(get_nouns_verbs_adjectives_adverbs_only(klexikon_article))

    # TODO: Include stats for paragraphs?
    print_stats(wiki_number_sentences, klexikon_number_sentences, "sentences")
    print_stats(wiki_number_tokens, klexikon_number_tokens, "tokens")

    # Calculate length-per-sentence for documents.
    sentence_lengths_wiki = [tokens / sentences for tokens, sentences in zip(wiki_number_tokens, wiki_number_sentences)]
    sentence_lengths_klexikon = [tokens / sentences for tokens, sentences in zip(klexikon_number_tokens, klexikon_number_sentences)]
    print(f"Wikipedia average sentence length: {np.mean(sentence_lengths_wiki):.2f} +/- {np.std(sentence_lengths_wiki):.2f}")
    print(f"Klexikon average sentence length:  {np.mean(sentence_lengths_klexikon):.2f} +/- {np.std(sentence_lengths_klexikon):.2f}")

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

    # Plot of the histograms

    # Set correct font size
    matplotlib.rc('xtick', labelsize=18)
    matplotlib.rc('ytick', labelsize=18)
    # set LaTeX font
    matplotlib.rcParams['mathtext.fontset'] = 'stix'
    matplotlib.rcParams['font.family'] = 'STIXGeneral'

    plt.hist(wiki_number_sentences, range=(0, 2000), bins=50, color='#1b9e77')
    plt.xlim([0, 1250])
    plt.ylim([0, 500])
    plt.axvline(np.mean(wiki_number_sentences), color='k', linestyle='dashed', linewidth=2)
    plt.axvline(np.mean(wiki_number_sentences) - np.std(wiki_number_sentences), color='k', linestyle='dotted', linewidth=1)
    plt.axvline(np.mean(wiki_number_sentences) + np.std(wiki_number_sentences), color='k', linestyle='dotted', linewidth=1)
    plt.axvline(np.median(wiki_number_sentences), color='#d95f02', linestyle='solid', linewidth=2)
    plt.savefig(f"./results/histogram_wiki.png")
    plt.show()
    plt.close()
    # Histo for Klexikon
    plt.hist(klexikon_number_sentences, range=(0, 200), bins=50, color='#1b9e77')
    plt.xlim([0, 125])
    plt.ylim([0, 500])
    plt.axvline(np.mean(klexikon_number_sentences), color='k', linestyle='dashed', linewidth=2)
    plt.axvline(np.mean(klexikon_number_sentences) - np.std(klexikon_number_sentences), color='k', linestyle='dotted', linewidth=1)
    plt.axvline(np.mean(klexikon_number_sentences) + np.std(klexikon_number_sentences), color='k', linestyle='dotted', linewidth=1)
    plt.axvline(np.median(klexikon_number_sentences), color='#d95f02', linestyle='solid', linewidth=2)
    plt.savefig(f"./results/histogram_klexikon.png")
    plt.show()
    plt.close()

    ratios = [wiki_value / klexikon_value for wiki_value, klexikon_value in zip(wiki_number_sentences, klexikon_number_sentences)]
    plt.hist(ratios, range=(0, 100), bins=66, color='#1b9e77')
    plt.xlim([0, 50])
    plt.ylim([0, 500])
    plt.axvline(np.mean(ratios), color='k', linestyle='dashed', linewidth=2)
    plt.axvline(np.mean(ratios) - np.std(ratios), color='k', linestyle='dotted', linewidth=1)
    plt.axvline(np.mean(ratios) + np.std(ratios), color='k', linestyle='dotted', linewidth=1)
    plt.axvline(np.median(ratios), color='#d95f02', linestyle='solid', linewidth=2)
    plt.savefig(f"./results/histogram_ratios.png")
    plt.show()
