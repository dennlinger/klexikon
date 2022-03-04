"""
Compare results with Rouge.
"""

import numpy as np
from tqdm import tqdm

from rouge_score import rouge_scorer
from rouge_score.scoring import BootstrapAggregator
from .utils import print_aggregate, evaluate_directory, directory_iterator
from ..baselines.baselines import get_rouge_scorer_with_cistem


def f1_score(score):
    calculated_f1 = 2 * (score.precision * score.recall) / (score.precision + score.recall)
    print(f"{calculated_f1:.4f}   {score.fmeasure:.4f}")


if __name__ == "__main__":

    # aggregator = BootstrapAggregator(confidence_interval=0.95)
    # # scorer = get_rouge_scorer_with_cistem()
    # scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=False)
    #
    # evaluate_directory(aggregator, scorer, pred_dir="./data/baselines/lead_3", gold_dir="./data/gold/")
    # print("\n------------------------------------")
    # print("Results for Lead-3 baseline:")
    # result = aggregator.aggregate()
    # print_aggregate(result)
    #
    # aggregator = BootstrapAggregator(confidence_interval=0.95)
    # scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=False)
    #
    # evaluate_directory(aggregator, scorer, pred_dir="./data/baselines/lead_k", gold_dir="./data/gold/")
    # print("\n------------------------------------")
    # print("Results for Lead-k baseline (Wikipedia's 'summary section'):")
    # result = aggregator.aggregate()
    # print_aggregate(result)
    #
    # aggregator = BootstrapAggregator(confidence_interval=0.95)
    # scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=False)
    #
    # evaluate_directory(aggregator, scorer, pred_dir="./data/baselines/lead_k_simplified", gold_dir="./data/gold/")
    # print("\n------------------------------------")
    # print("Results for Lead-k-simplified baseline (Wikipedia's 'summary section minus bracket texts'):")
    # result = aggregator.aggregate()
    # print_aggregate(result)

    aggregator = BootstrapAggregator(confidence_interval=0.95)
    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=False)

    # evaluate_directory(aggregator, scorer, pred_dir="./data/summaries", gold_dir="./data/gold/")
    # print("\n------------------------------------")
    # print("Results for LexRank/S-Transformer-simplified baseline:")
    # result = aggregator.aggregate()
    # print_aggregate(result)

    results = []
    for pred_fp, gold_fp in tqdm(directory_iterator("./data/summaries", "./data/gold")):
        with open(gold_fp) as f:
            gold = "".join(f.readlines())
        with open(pred_fp) as f:
            pred = "".join(f.readlines())

        results.append(scorer.score(gold, pred)["rouge1"])

    for result in results:
        f1_score(result)

    precisions = [score.precision for score in results]
    recalls = [score.recall for score in results]
    f1measures = [score.fmeasure for score in results]
    print(np.mean(precisions))
    print(np.mean(recalls))
    print(np.mean(f1measures))
    print(2 * (np.mean(precisions) * np.mean(recalls) / (np.mean(precisions) + np.mean(recalls))))

