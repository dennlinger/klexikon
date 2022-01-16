"""
This file takes the ~2950 samples from the preliminary data set and checks that the number of content paragraphs is
also appropriate. Since our histogram indicates that there are quite a few articles that don't have too many
content lines in themselves.
Further, we remove special characters, and create mappings for close variants (e.g., varying " forms),
to reduce the character set and make the "translations" more homogeneous. Note that this overwrites the "raw" corpus.
This should leave you with 2898 files in the end.
"""

from ..analysis.compare_offline_corpus import calculate_number_of_valid_lines
from ..baselines.utils import directory_iterator

from tqdm import tqdm

import string
import os


def clean_text(text):
    # Check for special characters

    # Actual occurring special characters and corresponding replacements
    text = text.replace("а", "a")
    text = text.replace("å", "a")
    text = text.replace("á", "a")
    text = text.replace("Á", "A")
    text = text.replace("ά", "a")
    text = text.replace("à", "a")
    text = text.replace("ā", "a")
    text = text.replace("â", "a")
    text = text.replace("α", "a")
    text = text.replace("ă", "a")
    text = text.replace("ã", "a")
    text = text.replace("ć", "c")
    text = text.replace("č", "c")
    text = text.replace("Č", "C")
    text = text.replace("Ç", "C")
    text = text.replace("ç", "c")
    text = text.replace("с", "c")
    text = text.replace("Đ", "D")
    text = text.replace("é", "e")
    text = text.replace("ē", "e")
    text = text.replace("е", "e")
    text = text.replace("ę", "e")
    text = text.replace("É", "E")
    text = text.replace("è", "e")
    text = text.replace("ë", "e")
    text = text.replace("ê", "e")
    text = text.replace("ě", "e")
    text = text.replace("Ǧ", "G")
    text = text.replace("ğ", "g")
    text = text.replace("ḥ", "h")
    text = text.replace("í", "i")
    text = text.replace("ī", "i")
    text = text.replace("ı", "i")
    text = text.replace("î", "i")
    text = text.replace("ί", "i")
    text = text.replace("ï", "i")
    text = text.replace("İ", "I")
    text = text.replace("ł", "l")
    text = text.replace("Ł", "L")
    text = text.replace("ñ", "n")
    text = text.replace("ń", "n")
    text = text.replace("ο", "o")
    text = text.replace("ō", "o")
    text = text.replace("ő", "ö")
    text = text.replace("ó", "o")
    text = text.replace("ό", "o")
    text = text.replace("ò", "o")
    text = text.replace("ô", "o")
    text = text.replace("ø", "o")
    text = text.replace("о", "o")
    text = text.replace("ό", "o")
    text = text.replace("р", "p")
    text = text.replace("ř", "r")
    text = text.replace("ś", "s")
    text = text.replace("š", "s")
    text = text.replace("Š", "S")
    text = text.replace("ș", "s")
    text = text.replace("ş", "s")
    text = text.replace("ẞ", "ß")
    text = text.replace("ú", "u")
    text = text.replace("ύ", "u")
    text = text.replace("ū", "u")
    text = text.replace("υ", "u")
    text = text.replace("ν", "v")
    text = text.replace("ý", "y")
    text = text.replace("у", "y")
    text = text.replace("ž", "z")
    text = text.replace("ž", "z")
    text = text.replace("Ž", "Z")
    text = text.replace("ź", "z")

    # Punctuation
    text = text.replace("‚", ",")
    # Dashes
    text = text.replace("–", "-")
    text = text.replace("−", "-")
    # Apostrophes and parentheses
    text = text.replace("’", "'")
    text = text.replace("ʾ", "'")
    text = text.replace("ʿ", "'")
    text = text.replace("′", "'")
    text = text.replace("`", "'")
    text = text.replace("‘", "'")
    text = text.replace("ʻ", "'")
    text = text.replace("„", '"')
    text = text.replace("“", '"')
    text = text.replace("‟", '"')
    text = text.replace("”", '"')
    text = text.replace("″", '"')
    text = text.replace("«", '"')
    text = text.replace("»", '"')

    # Others
    text = text.replace("→", "=")
    text = text.replace("≥", ">=")
    text = text.replace("±", "+/-")
    text = text.replace("\xad", "")  # "Soft hyphen" that is used for automated line breaks.
    text = text.replace("\xa0", " ")  # Non-breaking spaces. Doesn't matter for our format.
    text = text.replace("\u202f", " ")  # Another non-breaking space.
    text = text.replace("\u200b", " ")  # Zero-width space.
    text = text.replace("\t", " ")
    text = text.replace("…", "...")
    text = text.replace("·", "*")
    text = text.replace("•", "*")
    text = text.replace("⋅", "*")
    text = text.replace("²", "^2")
    text = text.replace("³", "^3")
    text = text.replace("×", "x")
    text = text.replace("†", "+")

    return text


def write_clean_text(lines, fp):
    new_text = []
    for line in lines:
        line = clean_text(line)
        new_line = ""
        for c in line:
            if c in valid_chars:
                new_line += c

        new_text.append(new_line)

    with open(fp, "w") as f:
        f.write("".join(new_text))


if __name__ == '__main__':
    valid_chars = string.ascii_letters + string.digits + string.punctuation + " " + "äöüßÄÖÜ\n§€°"
    print(valid_chars)
    wiki_dir = "./data/raw/wiki"
    klexikon_dir = "./data/raw/klexikon"

    occurrences = []
    for wiki_fp, klexikon_fp in tqdm(directory_iterator(wiki_dir, klexikon_dir)):
        with open(wiki_fp) as f:
            wiki_lines = f.readlines()
        with open(klexikon_fp) as f:
            klexikon_lines = f.readlines()

        wiki_num_sents = calculate_number_of_valid_lines(wiki_lines)
        klexikon_num_sents = calculate_number_of_valid_lines(klexikon_lines)

        # We previously only checked for 15 overall paragraphs, but some of those were headings.
        # This only removes 8 articles or so.
        if wiki_num_sents < 15:
            print(f"Article removed: {wiki_fp}")
            os.remove(wiki_fp)
            os.remove(klexikon_fp)

        # Remove article pairs where the Klexikon article is more than 150% of the length of the Wiki article.
        if wiki_num_sents * 1.5 < klexikon_num_sents:
            print(f"Article removed: {wiki_fp}")
            os.remove(wiki_fp)
            os.remove(klexikon_fp)

        write_clean_text(wiki_lines, wiki_fp)
        write_clean_text(klexikon_lines, klexikon_fp)

    """
    This code was used to determine the special characters by looking at the most frequent ones that aren't already
    in our cleaning function. Note that we did not want to use something like unidecode for two reasons:
        a) Unidecode has a GPL-2 license, which is not very user-friendly.
        b) It does not correctly treat German in particular. Correct "translations" for, e.g., "ä" would be "ae",
           but is only abridged to "a" instead. This behavior is similar in other libraries, unfortunately.
    """

    #     for line in wiki_lines:
    #         line = clean_text(line)
    #         for c in line:
    #             occurrences.append(c)
    #
    #     for line in klexikon_lines:
    #         line = clean_text(line)
    #         for c in line:
    #             occurrences.append(c)
    #
    # occurring_chars = Counter(occurrences).most_common(200)
    # for c in occurring_chars:
    #     if c[0] not in valid_chars:
    #         print(c)

    # Ignored are all characters that are not "clearly latin", i.e. can easily be matched to an ascii character.
    # This is mostly cyrillic, greek, etc. Anything that appears less than 100 times is ignored regardless.
