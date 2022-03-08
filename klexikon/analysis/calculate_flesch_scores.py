"""
Calculate Flesch reading-ease scores with textstat.
Note that the calculation for German slightly differs from the English baseline.
"""

from tqdm import tqdm

import numpy as np
import textstat
import os


def get_flesch_stats(directory):
    res = []
    for fn in tqdm(sorted(os.listdir(directory))):
        fp = os.path.join(directory, fn)
        with open(fp) as f:
            lines = f.readlines()
            text = " ".join(lines)
            text = text.replace("\n", "")  # line before already introduces spaces instead.

            res.append(textstat.textstat.flesch_reading_ease(text))

    return res


if __name__ == "__main__":
    # The full wiki article already has every line break and paragraph removed.
    wiki_fd = "./data/baselines_all_articles/full_wiki_article/"
    klexikon_fd = "./data/gold/"
    textstat.textstat.set_lang("de")

    wiki_values = get_flesch_stats(wiki_fd)
    klexikon_values = get_flesch_stats(klexikon_fd)

    print(f"Average scores for Wikipedia: {np.mean(wiki_values):.2f} +/- {np.std(wiki_values):.2f}")
    print(f"Average scores for Klexikon:  {np.mean(klexikon_values):.2f} +/- {np.std(klexikon_values):.2f}")
