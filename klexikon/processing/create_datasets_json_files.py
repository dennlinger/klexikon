"""
This script transforms the per-article files into three respective JSON files (train.json, validation.json, test.json),
which are uploaded to Huggingface Datasets.
"""

import json
import os

from tqdm import tqdm

from ..baselines.utils import directory_iterator, get_filename_from_article_title


def clean_text(lines):
    # We keep sentences in separate lines, which we want to maintain for the dataset.
    lines = [line.strip("\n ") for line in lines]

    lines = remove_empty_sections(lines)

    lines = remove_last_line_if_empty(lines)

    return lines


def remove_empty_sections(lines):
    """
    Mainly relevant for Wikipedia articles, this removes sections without any actual textual content.
    Notably, we leave in transfer from sections to subsections, subsections to subsubsections, etc.
    """
    new_lines = []

    curr_section_depth = "="
    curr_section_is_empty = True
    curr_section_lines = []

    for line in lines:
        # Encountering start of new section
        if line.startswith("="):
            # Current new section is a subsection, so we don't care if it is empty
            if len(curr_section_depth) < len(line.split(" ")[0]) or not curr_section_is_empty:
                new_lines.extend(curr_section_lines)
            # if it is a section of same depth, and there had not been any content, remove
            elif len(curr_section_depth) >= len(line.split(" ")[0]) and curr_section_is_empty:
                # don't add it to content, and reset for next block
                pass
            else:
                raise ValueError(f"Found uncovered edge case: "
                                 f"{curr_section_is_empty}, {curr_section_depth}, {curr_section_lines}")

            curr_section_is_empty = True
            curr_section_depth = line.split(" ")[0]  # only take the "===" part
            curr_section_lines = []

        curr_section_lines.append(line)
        # Mark relevant lines as textual content
        if line != "" and not line.startswith("="):
            curr_section_is_empty = False

    # Add last section
    if not curr_section_is_empty:
        new_lines.extend(curr_section_lines)

    return new_lines


def remove_last_line_if_empty(lines):
    if lines[-1] == "":
        return lines[:-1]
    else:
        return lines


if __name__ == '__main__':

    with open("./data/articles.json") as f:
        articles = json.load(f)

    # Make articles file searchable, but maintain original attributes
    articles = {get_filename_from_article_title(entry["title"]): entry for entry in articles}

    split_base_bath = "./data/splits/"
    out_path = "./data/"

    u_id = 0
    for subfolder in os.listdir(split_base_bath):
        wiki_dir = os.path.join(split_base_bath, subfolder, "wiki")
        klexikon_dir = os.path.join(split_base_bath, subfolder, "klexikon")

        output_samples = []
        # Clear output file
        with open(os.path.join(out_path, f"{subfolder}.json"), "w") as f:
            pass

        for wiki_fp, klexikon_fp in tqdm(directory_iterator(wiki_dir, klexikon_dir)):
            with open(wiki_fp) as f:
                wiki_lines = f.readlines()
            with open(klexikon_fp) as f:
                klexikon_lines = f.readlines()

            fn = wiki_fp.split("/")[-1]

            wiki_lines = clean_text(wiki_lines)
            klexikon_lines = clean_text(klexikon_lines)

            # Get meta information from the combined articles dictionary
            metadata = articles[fn]

            sample = {
                "u_id": u_id,
                "title": metadata["title"],
                "wiki_url": metadata["wiki_url"],
                "klexikon_url": metadata["klexikon_url"],
                "wiki_sentences": wiki_lines,
                "klexikon_sentences": klexikon_lines
            }

            u_id += 1

            with open(os.path.join(out_path, f"{subfolder}.json"), "a") as f:
                f.write(f"{json.dumps(sample, ensure_ascii=False)}\n")







