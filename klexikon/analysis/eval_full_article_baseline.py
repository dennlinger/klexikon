"""
We just want to verify that we don't accidentally get really good scores with the full articles.
"""

from rouge_score import rouge_scorer
from rouge_score.scoring import BootstrapAggregator
from .utils import print_aggregate, evaluate_directory

if __name__ == "__main__":

    aggregator = BootstrapAggregator(confidence_interval=0.95)
    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=False)

    evaluate_directory(aggregator, scorer, pred_dir="./data/baselines/full_wiki_article", gold_dir="./data/gold/")
    print("\n------------------------------------")
    print("Results for the full Wikipedia article (with paragraph separators and headings removed):")
    result = aggregator.aggregate()
    print_aggregate(result)
