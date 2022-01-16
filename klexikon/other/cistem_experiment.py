"""
Question from https://datascience.stackexchange.com/questions/57191/is-there-a-good-german-stemmer/
Ran experiments with the Cistem stemmer instead.
"""
from nltk.stem.cistem import Cistem
st = Cistem(case_insensitive=True)

token_groups = [(["experte", "Experte", "Experten", "Expertin", "Expertinnen"], []),
                (["geh", "gehe", "gehst", "geht", "gehen", "gehend"], []),
                (["gebäude", "Gebäude", "Gebäudes"], []),
                (["schön", "schöner", "schönsten"], ["schon"])]
header = "{:<15} [best expected: n/n| best variants: 1/n | overlap: m]: ...".format("name")
print(header)
print('-' * len(header))
for token_group, different_tokens in token_groups:
    print(different_tokens)
    stemmed_tokens = [st.stem(token) for token in token_group]
    different_tokens = [st.stem(token) for token in different_tokens]
    nb_expected = sum(1 for token in stemmed_tokens if token == token_group[0])
    nb_variants = len(set(stemmed_tokens))
    overlap = set(stemmed_tokens).intersection(set(different_tokens))
    print("{:<15} [as expected: {}/{}| variants: {}/{} | overlap: {}]: {}".format(token_group[0], nb_expected, len(token_group), nb_variants, len(token_group), len(overlap), stemmed_tokens))
