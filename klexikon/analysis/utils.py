from urllib.parse import unquote
from typing import List, Dict
from ..baselines.utils import directory_iterator


def get_klexikon_titles(file_location: str) -> List[str]:
    with open(file_location, "r") as f:
        urls = f.readlines()

    headlines = []
    for url in urls:
        # remove newline char, split at the "/wiki/", and insert spacing
        # Splitting only at "/" does not work, since some articles contain "/" in their titles, such as "AC/DC"
        article_title = unquote(url.strip().split("/wiki/")[-1]).replace("_", " ")
        headlines.append(article_title)
    return headlines


def get_klexikon_urls(file_location: str) -> List[str]:
    with open(file_location, "r") as f:
        urls = f.readlines()
    urls = [url.strip() for url in urls]
    return urls


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


def evaluate_directory(aggregator, scorer, pred_dir: str = "./data/baselines/lead_3", gold_dir: str = "./data/gold/"):
    """
    Adds ROUGE evaluations to the passed aggregator object, depending on the files in the prediction directory.
    :param aggregator:
    :param scorer:
    :param pred_dir:
    :param gold_dir:
    :return: None
    """
    for pred_fp, gold_fp in directory_iterator(pred_dir, gold_dir):
        with open(gold_fp) as f:
            gold = "".join(f.readlines())
        with open(pred_fp) as f:
            pred = "".join(f.readlines())

        aggregator.add_scores(scorer.score(gold, pred))
