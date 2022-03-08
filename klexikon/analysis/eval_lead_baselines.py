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

    evaluate_directory(aggregator, scorer, pred_dir="./data/baselines/lead_3", gold_dir="./data/gold/")
    print("\n------------------------------------")
    print("Results for Lead-3 baseline:")
    result = aggregator.aggregate()
    print_aggregate(result)

    aggregator = BootstrapAggregator(confidence_interval=0.95)
    scorer = get_rouge_scorer_with_cistem(fast=fast)
    # scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=False)

    evaluate_directory(aggregator, scorer, pred_dir="./data/baselines/lead_k", gold_dir="./data/gold/")
    print("\n------------------------------------")
    print("Results for Lead-k baseline (Wikipedia's 'summary section'):")
    result = aggregator.aggregate()
    print_aggregate(result)

    aggregator = BootstrapAggregator(confidence_interval=0.95)
    scorer = get_rouge_scorer_with_cistem(fast=fast)
    # scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=False)

    evaluate_directory(aggregator, scorer, pred_dir="./data/baselines/lead_k_simplified", gold_dir="./data/gold/")
    print("\n------------------------------------")
    print("Results for Lead-k-simplified baseline (Wikipedia's 'summary section minus bracket texts'):")
    result = aggregator.aggregate()
    print_aggregate(result)

    aggregator = BootstrapAggregator(confidence_interval=0.95)
    scorer = get_rouge_scorer_with_cistem(fast=fast)
    # scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=False)

    evaluate_directory(aggregator, scorer, pred_dir="./data/summaries", gold_dir="./data/gold/")
    print("\n------------------------------------")
    print("Results for LexRank/S-Transformer-simplified baseline:")
    result = aggregator.aggregate()
    print_aggregate(result)

    aggregator = BootstrapAggregator(confidence_interval=0.95)
    scorer = get_rouge_scorer_with_cistem(fast=fast)
    # scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=False)

    evaluate_directory(aggregator, scorer, pred_dir="./data/baselines/rouge2_fmeasure", gold_dir="./data/gold/")
    print("\n------------------------------------")
    print("Results for ROUGE-2 oracle (with F1 optimization):")
    result = aggregator.aggregate()
    print_aggregate(result)

    aggregator = BootstrapAggregator(confidence_interval=0.95)
    scorer = get_rouge_scorer_with_cistem(fast=fast)
    # scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=False)

    evaluate_directory(aggregator, scorer, pred_dir="./data/baselines/rouge2_precision", gold_dir="./data/gold/")
    print("\n------------------------------------")
    print("Results for ROUGE-2 oracle (with precision optimization):")
    result = aggregator.aggregate()
    print_aggregate(result)

    aggregator = BootstrapAggregator(confidence_interval=0.95)
    scorer = get_rouge_scorer_with_cistem(fast=fast)
    # scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=False)

    evaluate_directory(aggregator, scorer, pred_dir="./data/baselines/rouge2_recall", gold_dir="./data/gold/")
    print("\n------------------------------------")
    print("Results for ROUGE-2 oracle (with recall optimization):")
    result = aggregator.aggregate()
    print_aggregate(result)
