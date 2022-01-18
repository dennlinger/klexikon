"""
Script to generate sentence-aligned versions of the data.
"""

import os
from tqdm import tqdm
from typing import List

from sentence_transformers import SentenceTransformer, util
import torch

from ..analysis.utils import directory_iterator


def generate_sentence_ngrams(lines: List[str], n: int = 2) -> List[str]:
    """
    Generates up to n-gram pairs of sentences (within paragraphs only) of an article. E.g., for n=2,
    the source will include all "normal" single sentences, as well as a combination of two successive sentences.
    """
    all_combinations = []

    if n != 2:
        raise ValueError("ngrams of more than 2 currently not supported!")

    combination_candidate = ""
    for line in lines:
        line = line.strip("\n ")
        if line and not line.startswith("=="):
            all_combinations.append(line)

            if combination_candidate != "":
                all_combinations.append(f"{combination_candidate} {line}")

            combination_candidate = line

        else:  # This indicates a new paragraph
            combination_candidate = ""
    return all_combinations


if __name__ == '__main__':

    # TODO: Set correct device
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2", device=device)

    target_dir = "./data/aligned/"
    os.makedirs(target_dir, exist_ok=True)

    wiki_dir = "./data/raw/wiki"
    klexikon_dir = "./data/gold"  # Use gold data, because we would just do the same processing anyways

    for wiki_fp, klexikon_fp in tqdm(directory_iterator(wiki_dir, klexikon_dir)):
        with open(wiki_fp) as f:
            wiki_lines = f.readlines()[:20]
        with open(klexikon_fp) as f:
            klexikon_lines = f.readlines()[:10]

        wiki_ngram_sentences = generate_sentence_ngrams(wiki_lines)
        klexikon_lines = [line.strip("\n ") for line in klexikon_lines]

        # see https://www.sbert.net/docs/usage/semantic_textual_similarity.html
        # Compute embedding for both lists
        klexikon_embeddings = model.encode(klexikon_lines, convert_to_tensor=True)
        wiki_embeddings = model.encode(wiki_ngram_sentences, convert_to_tensor=True)

        # Compute cosine-similarities
        cosine_scores = util.cos_sim(klexikon_embeddings, wiki_embeddings)

        print(len(cosine_scores))
        break