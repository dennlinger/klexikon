"""
Since rouge expects basically line-by-line "gold summaries", we strip the Klexikon articles of any empty lines or
headings (both will be ignored in this simple scenario). Note that this information is still available in the raw
data format, and can therefore be used for other experiments.
"""

import os

if __name__ == '__main__':
    source_dir = "./data/raw/klexikon/"
    target_dir = "./data/gold/"

    os.makedirs(target_dir, exist_ok=True)

    for fn in sorted(os.listdir(source_dir)):
        in_fp = os.path.join(source_dir, fn)
        out_fp = os.path.join(target_dir, fn)

        with open(in_fp) as f:
            lines = f.readlines()

        gold_summary = []
        for line in lines:
            if line.strip("\n ") and not line.startswith("=="):
                gold_summary.append(line)

        with open(out_fp, "w") as f:
            f.write("".join(gold_summary))
