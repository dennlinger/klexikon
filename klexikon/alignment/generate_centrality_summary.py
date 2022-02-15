"""
Experimentation with models for summarization, based on a quick-and-dirty centrality embedding strategy.
"""
import pickle
import os

import torch
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

from ..analysis.utils import directory_iterator

if __name__ == '__main__':

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2", device=device)

    model.to(device)

    target_dir = "./data/embeddings/"
    os.makedirs(target_dir, exist_ok=True)

    wiki_dir = "./data/raw/wiki"
    klexikon_dir = "./data/gold"  # Use gold data, because we would just do the same processing anyways

    for wiki_fp, klexikon_fp in tqdm(directory_iterator(wiki_dir, klexikon_dir)):

        with open(wiki_fp) as f:
            wiki_lines = f.readlines()
        # with open(klexikon_fp) as f:
        #     klexikon_lines = f.readlines()

        wiki_lines = [line.strip("\n ") for line in wiki_lines if line.strip("\n ")]
        # TODO: Think about embedding entire paragraphs instead?
        wiki_embeddings = model.encode(wiki_lines, convert_to_tensor=True)

        fn = os.path.basename(wiki_fp).replace(".txt", ".pkl")
        with open(os.path.join(target_dir, fn), "wb") as f:
            pickle.dump(wiki_embeddings, f)

        break

