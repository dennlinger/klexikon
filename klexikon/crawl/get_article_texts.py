"""
With the retrieved URLs, we now try to get all the articles.
Turns out that there is a MediaWiki API in Klexikon, too, which we might be able to re-purpose for our articles.
"""
from functools import lru_cache
from typing import List, Union
import requests
import regex
import json
import os

from bs4 import BeautifulSoup
from tqdm import tqdm
import spacy



@lru_cache(maxsize=1)
def get_spacy_model(model_name: str = "de_core_news_md"):
    return spacy.load(model_name)


def get_klexikon_text(url: str) -> str:
    """
    Retrieve the text from a Klexikon article. Returned text will be a line-by-line sentence dataset.
    Paragraphs are indicated by an additional empty line in between. This function purposefully ignores caption texts,
    and only includes direct text blocks and headlines.
    :param url: URL of the Klexikon article.
    :return: Extracted text.
    """
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    body = soup.findAll('div', {'id': "mw-content-text"})[0]
    # Only direct <p> descendants of this element hold the core text.
    # Note that there might be other text in sub-level <p> tags, which can belong to descriptors of groups, such as:
    # Lists, image captions, etc. We ignore the latter, since they don't form well-defined paragraphs/sentences.
    # This notably reduces the content of elements quite a bit, but should be fine in the larger context.
    # Only other element types are headlines, which we manually include as well.
    extracted_tags = body.findAll(['h1', 'h2', 'h3', 'h4', 'p'], recursive=False)
    clean_paragraphs = []
    # Paragraphs are already conveniently inside a single tag element.
    for paragraph in extracted_tags:
        # Remove any stray newlines
        cleaned_text = paragraph.text.strip(" \n").replace("\n", " ")
        if cleaned_text:
            cleaned_text = add_headline_highlight(paragraph, cleaned_text)
            clean_paragraphs.append(cleaned_text)

    result_text = format_paragraphs_into_text(clean_paragraphs)
    return result_text


def get_wiki_text(url: str) -> Union[str, None]:
    """
    While Wikipedia technically provides a text extraction API, we use a similar extraction technique to the Klexikon
    articles, which allows us to employ similar pre-/post-processing steps. Unfortunately, Wikipedia is slightly more
    complex, which is why this requires a secondary function with largely the same structure.
    :param url: URL of the Wikipedia article.
    :return:
    """
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    # Slightly different level from Klexikon due to secondary parsing level?
    body = soup.findAll('div', {'class': "mw-parser-output"})[0]
    extracted_tags = body.findAll(['h1', 'h2', 'h3', 'h4', 'p'], recursive=False)
    clean_paragraphs = []
    for paragraph in extracted_tags:
        # Special care for Wikipedia tags...
        cleaned_text = clean_wiki_paragraph(paragraph.text)
        # Only append paragraphs with actual content
        if cleaned_text:
            cleaned_text = add_headline_highlight(paragraph, cleaned_text)
            clean_paragraphs.append(cleaned_text)

    # Sometimes the URL with the direct match is for disambiguations, see for example the page for "Aal".
    # While we know that Klexikon articles are correct, we can quickly gauge by the length of the articles.
    # Similarly, we want to ensure a minimum length for the reference articles, which this does, too.
    if len(clean_paragraphs) < 15:
        print(len(clean_paragraphs), url)
        return None

    result_text = format_paragraphs_into_text(clean_paragraphs)
    return result_text


def clean_wiki_paragraph(text: str) -> str:
    """
    Performs the following pre-processing steps to improve spaCy's sentence splitting performance,
    which was atrocious on the original extracted text. Specifically, perform the following steps:
    - Remove &nbsp; whitespaces, which are interpreted separately
    - Same processing steps as Klexikon (stripping of spaces, removal of newlines)
    - Remove text in square brackets (mostly assumed to be pronunciations, or references)
    - Merge several whitespaces into a single one.
    :param text:
    :return:
    """
    # Output formatting was not pretty for this, which is due to Beautifulsoup.
    text = text.replace(u"\xa0", u" ")
    # Klexikon stripping and replacement.
    text = text.strip(" \n").replace("\n", " ")
    # Remove text in square brackets. Weird formatting, because we want a greedy stop, otherwise it will take the
    # longest substring between any two square brackets.
    text = regex.sub(r"\[[^\]\[]*\]", "", text)
    # Remove several whitespaces after each other, mostly due to earlier removals
    text = regex.sub(r"\s{2,}", " ", text)

    return text


def add_headline_highlight(paragraph, text) -> str:
    if paragraph.name.startswith("h"):
        # This is the level, i.e. "h3" would evaluate to int("3")
        prefix = '=' * int(paragraph.name[-1])
        return f"{prefix} {text}"
    else:
        return text


def format_paragraphs_into_text(paragraphs: List[str]) -> str:
    # Separate sentences line-by-line, and add additional empty line for new paragraph.
    nlp = get_spacy_model()

    text = ""
    for paragraph in paragraphs:
        # Don't parse headlines
        if paragraph.startswith("=="):
            text += paragraph + "\n"
        # Everything else goes through spacy
        else:
            doc = nlp(paragraph)
            for sent in doc.sents:
                text += sent.text.strip(" ") + "\n"
        text += "\n"

    return text


def store_text(text: str, fp: str) -> None:
    with open(fp, "w") as f:
        f.write(text)


if __name__ == "__main__":
    articles_file = "./data/articles.json"
    with open(articles_file, "r") as f:
        articles = json.load(f)

    print(f"Extracting text for {len(articles)} articles.")

    # Create folders for texts if they don't exist yet
    klexikon_folder = "./data/raw/klexikon/"
    wiki_folder = "./data/raw/wiki/"
    os.makedirs(klexikon_folder, exist_ok=True)
    os.makedirs(wiki_folder, exist_ok=True)

    for article in tqdm(articles):
        fn = f"{article['title'].replace(' ', '_').replace('/', '_')}.txt"

        klexikon_out_fp = os.path.join(klexikon_folder, fn)
        # Skip processing of already existing files
        if not os.path.exists(klexikon_out_fp):
            klexikon_text = get_klexikon_text(article['klexikon_url'])
            store_text(klexikon_text, klexikon_out_fp)

        wiki_out_fp = os.path.join(wiki_folder, fn)
        if not os.path.exists(wiki_out_fp):
            wiki_text = get_wiki_text(article['wiki_url'])
            if wiki_text is None:
                continue  # Skip for now, so we can adjust the links and get back later.
            else:
                store_text(wiki_text, wiki_out_fp)
