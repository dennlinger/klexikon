"""
Similar to eval_lead_baselines.py, but evaluates the ROUGE oracle baselines.
"""
from rouge_score.scoring import BootstrapAggregator

from .utils import print_aggregate, evaluate_directory
from ..baselines.baselines import get_rouge_scorer_with_cistem


if __name__ == '__main__':
    fast = True

    aggregator = BootstrapAggregator(confidence_interval=0.95)
    scorer = get_rouge_scorer_with_cistem(fast=fast)
    # scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=False)

    evaluate_directory(aggregator, scorer, pred_dir="./data/baselines_all_articles/rouge2_fmeasure",
                       gold_dir="./data/gold/")
    print("\n------------------------------------")
    print("Results for ROUGE-2 oracle (with F1 optimization):")
    result = aggregator.aggregate()
    print_aggregate(result)

    aggregator = BootstrapAggregator(confidence_interval=0.95)
    scorer = get_rouge_scorer_with_cistem(fast=fast)
    # scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=False)

    evaluate_directory(aggregator, scorer, pred_dir="./data/baselines_all_articles/rouge2_precision",
                       gold_dir="./data/gold/")
    print("\n------------------------------------")
    print("Results for ROUGE-2 oracle (with precision optimization):")
    result = aggregator.aggregate()
    print_aggregate(result)

    aggregator = BootstrapAggregator(confidence_interval=0.95)
    scorer = get_rouge_scorer_with_cistem(fast=fast)
    # scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=False)

    evaluate_directory(aggregator, scorer, pred_dir="./data/baselines_all_articles/rouge2_recall",
                       gold_dir="./data/gold/")
    print("\n------------------------------------")
    print("Results for ROUGE-2 oracle (with recall optimization):")
    result = aggregator.aggregate()
    print_aggregate(result)