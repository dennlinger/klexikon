"""
Copying example from official lexrank package README
"""

from lexrank import LexRank
from lexrank.mappings.stopwords import STOPWORDS
from path import Path

# TODO: Replace regular TF-IDF with spacy sentence similarity
documents = []
documents_dir = Path('./data/raw/wiki_lexrank_train')

for file_path in documents_dir.files('*.txt'):
    with file_path.open(mode='rt', encoding='utf-8') as fp:
        documents.append(fp.readlines())

lxr = LexRank(documents, stopwords=STOPWORDS['de'])

with open("./data/raw/wiki_lexrank_test/Spiel.txt") as f:
    sentences = f.readlines()

sentences = [sentence.strip("\n ") for sentence in sentences]
summary = lxr.get_summary(sentences, summary_size=5, threshold=0.1)

