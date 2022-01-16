"""
Script to obtain the URLs of all main articles in the Klexikon space.
This should equal around 3150 articles (2021-03-15).
"""

from lxml import etree
from io import BytesIO
import requests
import os

# There are currently four overview pages that allow us to retrieve URLs for all articles.
# FIXME: The URLs will likely have to be adjusted for a new crawl, as they are direct links to the pagination sites.
overview_urls = [
    "https://klexikon.zum.de/wiki/Kategorie:Klexikon-Artikel",
    "https://klexikon.zum.de/index.php?title=Kategorie:Klexikon-Artikel&pagefrom=Globus#mw-pages",
    "https://klexikon.zum.de/index.php?title=Kategorie:Klexikon-Artikel&pagefrom=Orange#mw-pages",
    "https://klexikon.zum.de/index.php?title=Kategorie:Klexikon-Artikel&pagefrom=Weltkulturerbe#mw-pages"
]


def write_url(href, f):
    full_line = "https://klexikon.zum.de" + href + "\n"
    f.write(full_line)


if __name__ == "__main__":
    output_dir = "/home/dennis/klexikon/data/"
    article_file = os.path.join(output_dir, "article_urls.txt")
    parser = etree.HTMLParser()

    with open(article_file, "w") as f:

        for url in overview_urls:
            res = requests.get(url)

            tree = etree.parse(BytesIO(res.content), parser)
            content_div = tree.xpath("//div[contains(@class, 'mw-content-ltr')]")
            article_urls = content_div[0].xpath(".//li/a")

            for article in article_urls:
                write_url(article.attrib['href'], f)

    with open(article_file, "r") as f:
        # FIXME: This is likely inaccurate for the updated collection as well.
        assert len(f.readlines()) == 3150, "Incorrect number of files found!"
