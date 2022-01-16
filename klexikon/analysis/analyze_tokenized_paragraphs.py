"""
Evaluate the length distribution of paragraphs both in Klexikon and Wikipedia for tokenized inputs.
This is important to evaluate whether we can use models such as default BERT with 512 token input limits.
"""

from transformers import AutoTokenizer
from tqdm import tqdm

import numpy as np
import os


def group_to_paragraphs(lines):
    paragraphs = []

    curr_paragraph = ""
    for line in lines:
        clean_line = line.strip(" \n")
        if clean_line:
            curr_paragraph += f" {clean_line}"
        else:
            paragraphs.append(curr_paragraph)
            curr_paragraph = ""

    return paragraphs


if __name__ == '__main__':
    tokenizer = AutoTokenizer.from_pretrained("deepset/gbert-base")

    lengths = []

    fp = "./data/splits/train/wiki/"
    for fn in tqdm(sorted(os.listdir(fp))):
        with open(os.path.join(fp, fn)) as f:
            lines = f.readlines()

        paragraphs = group_to_paragraphs(lines)

        tokenized_paras = tokenizer(text=paragraphs, truncation=False)
        lengths.extend([len(para) for para in tokenized_paras.encodings])

    print(f"Wiki average length of paragraphs in BPE: {np.mean(lengths):.2f} +/- {np.std(lengths):.2f}")
    print(f"Wiki median length of paragraphs in BPE:  {np.median(lengths):.2f}")
    print(f"Wiki maximum length of paragraphs in BPE: {max(lengths)}")
    print(f"Wiki 95 percentile of paragraphs in BPE:  {np.percentile(lengths, 95)}")
    print(f"Wiki 99.9 percentile of paragraphs in BPE:{np.percentile(lengths, 99.9)}")
