"""
Similar to rouge_oracle, but instead utilizes a sentence similarity model to extract the highest overlap.
"""

import os
from operator import attrgetter

from tqdm import tqdm
from summaries.aligners import SentenceTransformerAligner

from .utils import directory_iterator
from .rouge_oracle import clean_lines

if __name__ == '__main__':
    summary_dir = "./data/splits/validation/klexikon"
    reference_dir = "./data/splits/validation/wiki/"

    out_dir = "./data/baselines_validation/stransformers-minilm/"
    os.makedirs(out_dir, exist_ok=True)

    aligner = SentenceTransformerAligner()

    for klexikon_fp, wiki_fp in tqdm(directory_iterator(source_dir=summary_dir,
                                                        target_dir=reference_dir)):
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
