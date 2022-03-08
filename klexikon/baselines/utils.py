"""
Simply utility to iterate through a directory containing text files.
"""
from typing import IO
import os


def directory_iterator(source_dir: str = "./data/raw/wiki/",
                       target_dir: str = "./data/baselines_all_articles/lead_3/") -> (IO, IO):
    for fn in sorted(os.listdir(source_dir)):
        in_fp = os.path.join(source_dir, fn)
        out_fp = os.path.join(target_dir, fn)

        yield in_fp, out_fp


def get_filename_from_article_title(title: str) -> str:
    return f"{title.replace(' ', '_').replace('/', '_')}.txt"
