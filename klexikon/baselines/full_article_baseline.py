"""
This is just a verification to see how similar articles are in general.
We basically employ the same steps as for the gold standard generation (removal of headlines and paragraph breaks).
"""
from .utils import directory_iterator

import os


def generate_full_article_summary(lines):
    clean_article = []
    for line in lines:
        if line.strip("\n ") and not line.startswith("=="):
            clean_article.append(line)

    return clean_article


if __name__ == "__main__":
    target_dir_full = "./data/baselines/full_wiki_article/"
    os.makedirs(target_dir_full, exist_ok=True)
    for in_fp, out_fp in directory_iterator(target_dir=target_dir_full):
        with open(in_fp) as f:
            lines = f.readlines()

        full_article = generate_full_article_summary(lines)
        with open(out_fp, "w") as f:
            f.write("".join(full_article))
