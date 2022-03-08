"""
A frequent baseline is to take the first three sentences of the article, which works especially well with news articles.
For our pre-processed data this should be relatively easy to extract, since it is already sentence-split, and we can
therefore simply copy the first few lines.
However, we first need to verify that these are properly split, since I already found some files that don't really
conform to this expectation. This has to do with some of the weird naming conventions of Wikipedia, which involves a
frequent use of ";" or bracket notation, which spaCy unfortunately interprets as some kind of sentence splitter.
See analysis/fix_lead_sentences.py for several fixes, and please execute that file first. Note that this will change
the underlying "raw" files in slight ways.

In contrast to news articles, Wikipedia actually provides a full *section* that is acting as a kind of summary.
In this example, we extract not a fixed number of (3) sentences, but instead take all content before the first "content
section" (we call this lead-k). Note that this can either lead to more *or less* content, since articles vary in length.
However, we can assume that there exists a correlation between the length of the Wikipedia and Klexikon articles, and
therefore consistently leads to a better performance.

Another baseline could be to take the same text as lead-k, but remove bracket content, since this is  "difficult" text.

TL;DR:  lead-3: Standard, first three sentences.
        lead-k: Take the entire introduction section of a Wiki page
        lead-k-simplified: Remove bracket content (round and square brackets) for "easier" text.
"""

import regex
import os

from .utils import directory_iterator


def generate_lead_3_summary(lines):
    lead_3 = []

    while len(lead_3) < 3 and lines:
        curr_line = lines.pop(0)

        if curr_line.strip("\n ") and not curr_line.startswith("=="):
            lead_3.append(curr_line)

    return lead_3


def generate_lead_k_summary(lines):
    lead_k = []

    while lines:
        curr_line = lines.pop(0)

        # This indicates the first content section
        if curr_line.startswith("=="):
            break

        if curr_line.strip("\n "):
            lead_k.append(curr_line)

    return lead_k


def generate_lead_k_simplified_summary(lines):
    lead_k_simplified = []

    while lines:
        curr_line = lines.pop(0)

        # This indicates the first content section
        if curr_line.startswith("=="):
            break

        if curr_line.strip("\n "):
            clean_line = strip_bracket_content(curr_line)
            # TODO: This doesn't capture all resulting whitespace issues, since there is something like
            #  "this particular model (in brackets), ...", which results in a space between "model" and ",".
            clean_line = regex.sub(r"\s{2,}", " ", clean_line)
            lead_k_simplified.append(clean_line)
    return lead_k_simplified


def strip_bracket_content(line: str) -> str:
    # Need to differentiate between parentheses and square brackets.
    parentheses_close_idx = 0
    parentheses_offset = 0
    square_bracket_close_idx = 0
    square_bracket_offset = 0

    # Iterate backwards so we can remove content on the fly
    backwards_idx_iter = range(len(line)-1, -1, -1)
    for idx, char in zip(backwards_idx_iter, line[::-1]):
        if char == ")":
            if parentheses_offset == 0:
                parentheses_close_idx = idx + 1
            parentheses_offset += 1
        # Check for larger > 0 to work with nested parentheses
        elif char == "(" and parentheses_offset > 0:
            if parentheses_offset == 1:
                # cut out bracket part from line
                line = line[:idx] + line[parentheses_close_idx:]
            parentheses_offset -= 1

        if char == "]":
            if square_bracket_offset == 0:
                square_bracket_close_idx = idx + 1
            square_bracket_offset += 1
        elif char == "[" and square_bracket_offset > 0:
            if square_bracket_offset == 1:
                # cut out bracket part from line
                line = line[:idx] + line[square_bracket_close_idx:]
            parentheses_offset -= 1

    return line


if __name__ == "__main__":
    target_dir_3 = "./data/baselines_all_articles/lead_3/"
    os.makedirs(target_dir_3, exist_ok=True)
    for in_fp, out_fp in directory_iterator(target_dir=target_dir_3):
        with open(in_fp) as f:
            lines = f.readlines()

        lead_3 = generate_lead_3_summary(lines)
        with open(out_fp, "w") as f:
            f.write("".join(lead_3))

    target_dir_k = "./data/baselines_all_articles/lead_k"
    os.makedirs(target_dir_k, exist_ok=True)
    for in_fp, out_fp in directory_iterator(target_dir=target_dir_k):
        with open(in_fp) as f:
            lines = f.readlines()

        lead_k = generate_lead_k_summary(lines)
        with open(out_fp, "w") as f:
            f.write("".join(lead_k))

    target_dir_k_simplified = "./data/baselines_all_articles/lead_k_simplified"
    os.makedirs(target_dir_k_simplified, exist_ok=True)
    for in_fp, out_fp in directory_iterator(target_dir=target_dir_k_simplified):

        with open(in_fp) as f:
            lines = f.readlines()

        lead_k_simplified = generate_lead_k_simplified_summary(lines)

        with open(out_fp, "w") as f:
            f.write("".join(lead_k_simplified))