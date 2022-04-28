"""
Script computing various baselines with the sumy extractive summarizaiton package.
Similar to lexrank summaries, we use the mean target number of sentences (25) as a reference value.
"""
import os

from tqdm import tqdm
from sumy.summarizers import luhn, lsa, sum_basic
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from .sumy_baselines_on_splits import get_summarizer, sumy_clean_lines


if __name__ == '__main__':
    lang = "german"
    num_summary_sentences = 25  # Corresponds to the mean of summary lengths

    stemmer = Stemmer(lang)

    # for method in ["sumbasic"]:  # Current bug in sumy!!
    for method in ["luhn", "lsa", "sumbasic"]:
        # Summarizer stays same for both test and validation
        summarizer = get_summarizer(method)

        # Set appropriate folders based on combinations
        source_dir = f"./data/raw/wiki"
        out_dir = f"./data/baselines_all_articles/sumy_{method}"
        os.makedirs(out_dir, exist_ok=True)

        for fn in tqdm(sorted(os.listdir(source_dir))):
            # File reading
            with open(os.path.join(source_dir, fn)) as f:
                lines = sumy_clean_lines(f.readlines())

            # Parse text and summarize
            parser = PlaintextParser.from_string(lines, Tokenizer(lang))
            res = summarizer(parser.document, num_summary_sentences)

            # Write out summary
            with open(os.path.join(out_dir, fn), "w") as f:
                f.write("\n".join([sentence._text for sentence in res]))
