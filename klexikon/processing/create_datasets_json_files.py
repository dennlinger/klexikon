"""
This script transforms the per-article files into three respective JSON files (train.json, validation.json, test.json),
which are uploaded to Huggingface Datasets.
"""

import json
import os

from tqdm import tqdm

from ..baselines.utils import directory_iterator, get_filename_from_article_title

if __name__ == '__main__':

    with open("./data/articles.json") as f:
        articles = json.load(f)

    # Make articles file searchable, but maintain original attributes
    articles = {get_filename_from_article_title(entry["title"]): entry for entry in articles}

    split_base_bath = "./data/splits/"
    out_path = "./data/"

    u_id = 0
    for subfolder in os.listdir(split_base_bath):
        wiki_dir = os.path.join(split_base_bath, subfolder, "wiki")
        klexikon_dir = os.path.join(split_base_bath, subfolder, "klexikon")

        output_json = []
        for wiki_fp, klexikon_fp in tqdm(directory_iterator(wiki_dir, klexikon_dir)):
            with open(wiki_fp) as f:
                wiki_lines = f.readlines()
            with open(klexikon_fp) as f:
                klexikon_lines = f.readlines()

            fn = wiki_fp.split("/")[-1]

            # We keep sentences in separate lines, which we want to maintain for the dataset.
            wiki_lines = [line.strip("\n ") for line in wiki_lines]
            klexikon_lines = [line.strip("\n ") for line in klexikon_lines]

            # Get meta information from the combined articles dictionary
            metadata = articles[fn]

            sample = {
                "u_id": u_id,
                "title": metadata["title"],
                "wiki_url": metadata["wiki_url"],
                "klexikon_url": metadata["klexikon_url"],
                "wiki_sentences": wiki_lines,
                "klexikon_sentences": klexikon_lines
            }

            output_json.append(sample)
            u_id += 1

        with open(os.path.join(out_path, f"{subfolder}.json"), "w") as f:
            json.dump(output_json, f, indent=2, ensure_ascii=False)






