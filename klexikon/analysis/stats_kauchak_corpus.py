"""
Computing additional supporting stats from the Kauchak paper
"""

import pandas as pd

from .compare_offline_corpus import print_stats


def get_token_lengths(df):
    token_lengths = [0]
    prev_article_title = next(df.iterrows())[1][0]
    for row in df.iterrows():
        title, _, sentence = row[1]
        if title == prev_article_title:
            if isinstance(sentence, str):
                token_lengths[-1] += len(sentence.split(" "))
        else:
            # We avoid zero division errors that way.
            #     print(prev_article_title, row)
            #     token_lengths[-1] += 1
            prev_article_title = title
            if token_lengths[-1] == 0:
                continue

            token_lengths.append(0)
            if isinstance(sentence, str):
                token_lengths[-1] += len(sentence.split(" "))

    return token_lengths


if __name__ == '__main__':
    normal_file = "./data/kauchak/normal.txt"
    simple_file = "./data/kauchak/simple.txt"

    df_normal = pd.read_csv(normal_file, header=None, sep="\t")
    df_simple = pd.read_csv(simple_file, header=None, sep="\t")

    # group by article title, which gives us the number of sentences per article in this data format.
    normal_groups = df_normal.groupby(0)[1].count()
    simple_groups = df_simple.groupby(0)[1].count()

    # print stats
    print_stats(list(normal_groups), list(simple_groups), unit="kauchak_sentences")

    normal_token_lengths = get_token_lengths(df_normal)
    simple_token_lengths = get_token_lengths(df_simple)

    print_stats(normal_token_lengths, simple_token_lengths, unit="kauchak_tokens")





