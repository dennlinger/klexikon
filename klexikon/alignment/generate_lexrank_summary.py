"""
Adaption of the sentence-transformers example to work with our (pre-split) dataset.
Notably, this also contains much longer input texts, which requires longer computation, due to square matrices.
"""

import os

import numpy as np
import pickle
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

from .LexRank import degree_centrality_scores


def remove_empty_lines_and_headings(text):
    return [line.strip("\n ") for line in text if line.strip("\n ") and not line.startswith("=")]


if __name__ == '__main__':
    num_summary_sentences = 10
    model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")

    base_dir = "./data/raw/wiki/"
    out_dir = "./data/summaries/"
    os.makedirs(out_dir, exist_ok=True)

    index_positions = []

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

        # TODO: Figure out whether sorting makes sense here? We assume that Wikipedia has some sensible structure.
        #   Otherwise, reversing would be enough to get the job done and get the most similar sentences first.
        # Scores are originally in ascending order
        # list(most_central_indices).reverse()
        most_central_indices = sorted(list(most_central_indices))

        index_positions.append(most_central_indices)
        summary = [lines[idx] for idx in most_central_indices]
        with open(os.path.join(out_dir, fn), "w") as f:
            f.write("\n".join(summary))
        # print(f"Summary for {fn}:")
        # for idx in most_central_indices:
        #     print(lines[idx])

    with open("./results/positions.pkl", "wb") as f:
        pickle.dump(index_positions, f)