"""
Adaption of the sentence-transformers example to work with our (pre-split) dataset.
Notably, this also contains much longer input texts, which requires longer computation, due to square matrices.
"""

import os

import numpy as np
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from tqdm import tqdm

from .LexRank import degree_centrality_scores


def remove_empty_lines_and_headings(text):
    return [line.strip("\n ") for line in text if line.strip("\n ") and not line.startswith("=")]


if __name__ == '__main__':
    num_summary_sentences = 5
    model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")

    base_dir = "./data/raw/wiki/"
    for fn in tqdm(sorted(os.listdir(base_dir))):
        fp = os.path.join(base_dir, fn)

        with open(fp) as f:
            lines = f.readlines()

        lines = remove_empty_lines_and_headings(lines)

        # Use tensor instead of numpy to get single element
        embeddings = model.encode(lines, convert_to_tensor=True)

        self_similarities = cos_sim(embeddings, embeddings).numpy()

        centrality_scores = degree_centrality_scores(self_similarities, threshold=None, increase_power=True)

        # Use argpartition instead of argsort for faster sorting, since we only need k << n sentences.
        # most_central_indices = np.argsort(-centrality_scores)
        most_central_indices = np.argpartition(centrality_scores, -num_summary_sentences)[-num_summary_sentences:]
        # Scores are originally in ascending order
        list(most_central_indices).reverse()

        print(f"Summary for {fn}:")
        for idx in most_central_indices:
            print(lines[idx])
