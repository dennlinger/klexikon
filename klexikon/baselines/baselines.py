"""
Consolidation file for various baselines for the split data.
Note that these should not require
"""

from argparse import ArgumentParser, ArgumentTypeError
from typing import List
from tqdm import tqdm
import pathlib
import os

from rouge_score.scoring import BootstrapAggregator, Score
from rouge_score.rouge_scorer import RougeScorer
from nltk.stem.cistem import Cistem

from .lead_baselines import generate_lead_3_summary, generate_lead_k_simplified_summary
from .full_article_baseline import generate_full_article_summary
from ..analysis.utils import print_aggregate
from .utils import directory_iterator
from ..GeRouge import GeRouge


def get_args():
    parser = ArgumentParser()
    parser.add_argument("--method", choices=["lead-3", "lead-k", "full"], default="lead-3",
                        help="Available summarization methods. Currently implements lead baselines only.")
    parser.add_argument("--rouge_scorer", choices=["GeRouge", "GeRouge-Cistem", "Rouge", "Rouge-Cistem"],
                        default="Rouge-Cistem", help="Which ROUGE scoring method to use.")
    parser.add_argument("--folder", choices=["train", "val", "test"], default="train",
                        help="Choice which part of the data should be evaluated.")
    parser.add_argument("--use-rouge-stemming", const=True, action="store_const",
                        help="Enables stemming when evaluating with ROUGE. Note that some scoring methods should "
                             "return the same without stemming but otherwise don't.")

    return parser.parse_args()


def get_rouge_scorer(args):
    if args.rouge_scorer == "GeRouge":
        return GeRougeWrapper(args)
    elif args.rouge_scorer == "GeRouge-Cistem":
        if not args.use_rouge_stemming:
            raise KeyError("Cannot use GeRouge-Cistem without stemming option enabled.")
        return get_GeRouge_scorer_with_cistem(args)
    elif args.rouge_scorer == "Rouge":
        return RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=args.use_rouge_stemming)
    elif args.rouge_scorer == "Rouge-Cistem":
        if not args.use_rouge_stemming:
            raise KeyError("Cannot use Rouge-Cistem without stemming option enabled.")
        return get_rouge_scorer_with_cistem()
    else:
        raise NotImplementedError("Invalid ROUGE scorer choice.")


class GeRougeWrapper:
    """
    To allow for a unified call with the "regular" Rouge class from Google Research, this function wraps
    a convenience layer around the GeRouge implementation that combines RougeN and RougeL calls.
    :return:
    """
    def __init__(self, args):
        self.scorer = GeRouge(alpha=0.5, stemming=args.use_rouge_stemming, split_compounds=True, minimal_mode=False)

    def score(self, target, prediction):
        """
        Function interface copied from other library.
        :param target: Ground truth summary.
        :param prediction: Predicted summary.
        :return: Rouge-1, Rouge-2 and Rouge-L P/R/F1 in the same format as Google Research.
        """
        rouge1, rouge2 = self.scorer.rouge_n(target, prediction)
        rougeL = self.scorer.rouge_l(target, prediction)

        return {"rouge1": Score(*rouge1), "rouge2": Score(*rouge2), "rougeL": Score(*rougeL)}


def get_GeRouge_scorer_with_cistem(args):
    scorer = GeRougeWrapper(args)
    stemmer = Cistem(case_insensitive=True)  # TODO: Is this really the best for insensitive?
    scorer.scorer.stemmer = stemmer

    return scorer


def get_rouge_scorer_with_cistem(fast=False):
    """
    Replaces the standard Porter stemmer, which works best on English, with the Cistem stemmer, which was specifically
    designed for the German language.
    :return: RougeScorer object with replaced stemmer.
    """
    # Skip LCS computation for 10x speedup during debugging.
    if fast:
        scorer = RougeScorer(["rouge1", "rouge2"], use_stemmer=True)
    else:
        scorer = RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    stemmer = Cistem(case_insensitive=True)  # Insensitive because RougeScorer lowercases anyways.
    scorer._stemmer = stemmer  # Certainly not best practice, but better than re-writing the package ;-)

    return scorer


def get_gold_reference(fp: str) -> List[str]:
    with open(fp) as f:
        lines = f.readlines()

    gold_summary = []
    for line in lines:
        if line.strip("\n ") and not line.startswith("=="):
            gold_summary.append(line)

    return gold_summary


if __name__ == '__main__':
    args = get_args()
    aggregator = BootstrapAggregator(confidence_interval=0.95)
    scorer = get_rouge_scorer(args)

    curr_folder = pathlib.Path(__file__).parent.parent.parent.absolute()
    eval_folder = os.path.join(curr_folder, "data", "splits", args.folder)

    for fp_source, fp_target in tqdm(directory_iterator(os.path.join(eval_folder, "wiki"),
                                                        os.path.join(eval_folder, "klexikon"))):

        with open(fp_source) as f:
            lines_source = f.readlines()

        if args.method == "lead-3":
            prediction = generate_lead_3_summary(lines_source)
        elif args.method == "lead-k":
            prediction = generate_lead_k_simplified_summary(lines_source)
        elif args.method == "full":
            prediction = generate_full_article_summary(lines_source)
        else:
            raise NotImplementedError("Summarization method not supported!")

        # Methods don't remove newlines, since we originally write them to file.
        prediction = " ".join([line.strip("\n ") for line in prediction])
        reference = " ".join([line.strip("\n ") for line in get_gold_reference(fp_target)])

        aggregator.add_scores(scorer.score(reference, prediction))

    print(f"ROUGE scores for {args.method} baseline:")
    print_aggregate(aggregator.aggregate())
