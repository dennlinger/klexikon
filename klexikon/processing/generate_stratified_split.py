"""
The idea is that we create a 2D grid, where we have different rectangles that represent our bins

                    length of the wikipedia article
200 --------------------------------------------------------------
    |                      |                    |                |
    |                      |                    |                |
    |                      |                    |                |
    |                      |                    |                |
    |                      |                    |                |  length
100 --------------------------------------------------------------  of
    |                      |                    |                |  Klexikon
    |                      |                    |                |  article
    |                      |                    |                |
    |                      |                    |                |
    |                      |                    |                |
0   --------------------------------------------------------------
    0                    1000                 2000             3000


Sampling a stratified development and test set is then done by iterating through all rectangles and drawing
a random sample from this sector. The idea would be to also weigh these rectangles by the number of samples in them.
"""

from ..analysis.compare_offline_corpus import calculate_number_of_valid_lines
from ..baselines.utils import directory_iterator

from collections import defaultdict
from shutil import copyfile
from tqdm import tqdm
import numpy as np
import os


def write_samples(files, name="train"):
    klexikon_target_fp = f"./data/splits/{name}/klexikon/"
    wiki_target_fp = f"./data/splits/{name}/wiki/"
    os.makedirs(klexikon_target_fp, exist_ok=True)
    os.makedirs(wiki_target_fp, exist_ok=True)

    klexikon_source_fp = "./data/raw/klexikon/"
    wiki_source_fp = "./data/raw/wiki/"
    for fp in files:
        fn = fp.split("/wiki/")[-1]

        copyfile(os.path.join(klexikon_source_fp, fn), os.path.join(klexikon_target_fp, fn))
        copyfile(os.path.join(wiki_source_fp, fn), os.path.join(wiki_target_fp, fn))


if __name__ == '__main__':
    wiki_dir = "./data/raw/wiki"
    klexikon_dir = "./data/raw/klexikon"
    wiki_block_size = 100
    klexikon_block_size = 10

    rng = np.random.default_rng(18052021)

    # Keep those variables separated, since we might want different splits
    val_fraction = 0.1
    test_fraction = 0.1

    grid = defaultdict(lambda: defaultdict(list))

    for wiki_fp, klexikon_fp in tqdm(directory_iterator(wiki_dir, klexikon_dir)):
        with open(wiki_fp) as f:
            wiki_lines = f.readlines()
        with open(klexikon_fp) as f:
            klexikon_lines = f.readlines()

        wiki_num_sents = calculate_number_of_valid_lines(wiki_lines)
        klexikon_num_sents = calculate_number_of_valid_lines(klexikon_lines)

        # Store in a "scaled-down" version of the grid
        grid[wiki_num_sents // wiki_block_size][klexikon_num_sents // klexikon_block_size].append(wiki_fp)

    train_files = []
    val_files = []
    test_files = []

    # Sample based on the fractions for each grid block.
    for _, klexikon_dimension in grid.items():
        for _, block in klexikon_dimension.items():
            val_samples = int(round(val_fraction * len(block)))
            test_samples = int(round(test_fraction * len(block)))

            # Sample a random order from all available files.
            drawn_samples = rng.choice(block, len(block), replace=False)
            val_files.extend(drawn_samples[:val_samples])
            test_files.extend(drawn_samples[val_samples:val_samples+test_samples])
            # Remainder is assigned as training files.
            train_files.extend(drawn_samples[val_samples+test_samples:])

    write_samples(train_files, "train")
    write_samples(val_files, "val")
    write_samples(test_files, "test")
