"""
Evaluates all baselines that are computed on the validation set, by iterating through the folders available there.
"""
import os

from rouge_score.scoring import BootstrapAggregator

from .utils import print_aggregate, evaluate_directory
from ..baselines.baselines import get_rouge_scorer_with_cistem

if __name__ == '__main__':
    fast = False
    base_dir = "./data/baselines_validation"

    scorer = get_rouge_scorer_with_cistem(fast=fast)
    # scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=False)
    for file_like in os.listdir(base_dir):
        # Ensure we're skipping anything that isn't a directory
        subdir = os.path.join(base_dir, file_like)
        if not os.path.isdir(subdir):
            continue

        # Compute scores
        aggregator = BootstrapAggregator(confidence_interval=0.95)

        evaluate_directory(aggregator, scorer, pred_dir=subdir, gold_dir="./data/gold/")
        print("\n------------------------------------")
        print(f"Results for {subdir}:")
        result = aggregator.aggregate()
        print_aggregate(result)