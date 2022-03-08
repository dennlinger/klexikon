"""
We just want to verify that we don't accidentally get really good scores with the full articles.
"""

from rouge_score import rouge_scorer
from rouge_score.scoring import BootstrapAggregator
from .utils import print_aggregate, evaluate_directory
from ..baselines.baselines import get_rouge_scorer_with_cistem

if __name__ == "__main__":

    aggregator = BootstrapAggregator(confidence_interval=0.95)
    scorer = get_rouge_scorer_with_cistem()

    evaluate_directory(aggregator,
                       scorer,
                       pred_dir="./data/baselines_all_articles/full_wiki_article",
                       gold_dir="./data/gold/")
    print("\n------------------------------------")
    print("Results for the full Wikipedia article (with paragraph separators and headings removed):")
    result = aggregator.aggregate()
    print_aggregate(result)
