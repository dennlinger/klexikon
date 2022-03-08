"""
Create ROUGE-2 maximizing baselines, with all three objectives (precision, recall, fmeasure).
"""
import os
from operator import attrgetter

from tqdm import tqdm
from summaries.aligners import Rouge2Aligner

from .utils import directory_iterator


def clean_lines(lines):
    new_lines = []
    for line in lines:
        clean_line = line.strip("\n ")
        if clean_line != "" and not clean_line.startswith("="):
            new_lines.append(clean_line)

    return new_lines


if __name__ == '__main__':

    for metric in ["precision", "recall", "fmeasure"]:
        aligner = Rouge2Aligner(metric)

        # Create necessary output directory
        out_dir = f"./data/baselines/rouge2_{metric}"
        os.makedirs(out_dir, exist_ok=True)

        for klexikon_fp, wiki_fp in tqdm(directory_iterator(source_dir="./data/raw/klexikon/",
                                                            target_dir="./data/raw/wiki/")
                                         ):
            fn = os.path.basename(klexikon_fp)
            with open(klexikon_fp) as f:
                klexikon_lines = clean_lines(f.readlines())

            with open(wiki_fp) as f:
                wiki_lines = clean_lines(f.readlines())

            # Find alignment maximizing this particular objective
            result = aligner.extract_source_sentences(summary=klexikon_lines, reference=wiki_lines)

            ordered_result = sorted(result, key=attrgetter("relative_position"))

            result_text = []
            # TODO: For actual sentence alignments, probably preserve matching and order!!!
            for sentence in ordered_result:
                # Avoid adding a sentence multiple times.
                # Set conversion would not guarantee order, this is why we do it this way.
                if sentence.sentence not in result_text:
                    result_text.append(sentence.sentence)

            # Write results
            with open(os.path.join(out_dir, fn), "w") as f:
                f.write("\n".join(result_text))




