"""
Experimentation for faster ROUGE score computation.
TL;DR: Removing ROUGE-L for debugging already gains significant speedups.

This script needs to be able to implement some of the functions at the top-level, since otherwise the profiler
won't work.
"""
import os
from typing import Dict, List

from rouge_score.rouge_scorer import RougeScorer
from rouge_score.scoring import BootstrapAggregator
from nltk.stem import Cistem
from tqdm import tqdm


def get_rouge_scorer_with_cistem():
    """
    Replaces the standard Porter stemmer, which works best on English, with the Cistem stemmer, which was specifically
    designed for the German language.
    :return: RougeScorer object with replaced stemmer.
    """
    scorer = RougeScorer(["rouge1", "rouge2"], use_stemmer=True)
    stemmer = Cistem(case_insensitive=True)  # Insensitive because RougeScorer lowercases anyways.
    scorer._stemmer = stemmer  # Certainly not best practice, but better than re-writing the package ;-)

    return scorer


def print_aggregate(result: Dict) -> None:
    for key, value_set in result.items():
        print(f"----------------{key} ---------------------")
        print(f"Precision | "
              f"low: {value_set.low.precision * 100:5.2f}, "
              f"mid: {value_set.mid.precision * 100:5.2f}, "
              f"high: {value_set.high.precision * 100:5.2f}")
        print(f"Recall    | "
              f"low: {value_set.low.recall * 100:5.2f}, "
              f"mid: {value_set.mid.recall * 100:5.2f}, "
              f"high: {value_set.high.recall * 100:5.2f}")
        print(f"F1        | "
              f"low: {value_set.low.fmeasure * 100:5.2f}, "
              f"mid: {value_set.mid.fmeasure * 100:5.2f}, "
              f"high: {value_set.high.fmeasure * 100:5.2f}")


def parallel_compute_scores(args: List[str]):
    gold_fp, pred_fp = args

    scorer = get_rouge_scorer_with_cistem()

    with open(gold_fp) as f:
        gold = "".join(f.readlines())
    with open(pred_fp) as f:
        pred = "".join(f.readlines())

    return scorer.score(gold, pred)


if __name__ == '__main__':
    gold_dir = "../data/raw/klexikon"
    system_dir = "../data/baselines/rouge2_fmeasure"

    aggregator = BootstrapAggregator(confidence_interval=0.95)
    scorer = get_rouge_scorer_with_cistem()

    for fn in tqdm(sorted(os.listdir(gold_dir))):
        gold_fp = os.path.join(gold_dir, fn)
        pred_fp = os.path.join(system_dir, fn)

        with open(gold_fp) as f:
            gold = "".join(f.readlines())
        with open(pred_fp) as f:
            pred = "".join(f.readlines())

        aggregator.add_scores(scorer.score(gold, pred))

    result = aggregator.aggregate()
    print_aggregate(result)


