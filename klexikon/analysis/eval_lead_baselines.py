"""
Compute baseline ROUGE scores
"""
from rouge_score.scoring import BootstrapAggregator

from .utils import print_aggregate, evaluate_directory
from ..baselines.baselines import get_rouge_scorer_with_cistem


if __name__ == "__main__":
    fast = True

    aggregator = BootstrapAggregator(confidence_interval=0.95)
    scorer = get_rouge_scorer_with_cistem(fast=fast)
    # scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=False)

    evaluate_directory(aggregator, scorer, pred_dir="./data/baselines_all_articles/lead_3", gold_dir="./data/gold/")
    print("\n------------------------------------")
    print("Results for Lead-3 baseline:")
    result = aggregator.aggregate()
    print_aggregate(result)

    aggregator = BootstrapAggregator(confidence_interval=0.95)
    scorer = get_rouge_scorer_with_cistem(fast=fast)
    # scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=False)

    evaluate_directory(aggregator, scorer, pred_dir="./data/baselines_all_articles/lead_k", gold_dir="./data/gold/")
    print("\n------------------------------------")
    print("Results for Lead-k baseline (Wikipedia's 'summary section'):")
    result = aggregator.aggregate()
    print_aggregate(result)

    aggregator = BootstrapAggregator(confidence_interval=0.95)
    scorer = get_rouge_scorer_with_cistem(fast=fast)
    # scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=False)

    evaluate_directory(aggregator, scorer, pred_dir="./data/baselines_all_articles/lead_k_simplified",
                       gold_dir="./data/gold/")
    print("\n------------------------------------")
    print("Results for Lead-k-simplified baseline (Wikipedia's 'summary section minus bracket texts'):")
    result = aggregator.aggregate()
    print_aggregate(result)

