# Klexikon: A German Dataset for Joint Summarization and Simplification
**Dennis Aumiller and Michael Gertz**  
Heidelberg University  

*Accepted at LREC 2022*  
A preprint version of the paper can be found on [arXiv](https://arxiv.org/abs/2201.07198)!  
For easy access, we have also made the dataset available on [Huggingface Datasets](https://huggingface.co/datasets/dennlinger/klexikon)!

-------------------------------------------------------------------------------------------
## Data Availability
To use data in your experiments, we suggest the existing training/validation/test split, available in [`./data/splits/`](./data/splits).
This split has been generated with a stratified sampling strategy (based on document lengths) and a 80/10/10 split, which ensure that the samples are somewhat evenly distributed.

Alternatively, please refer to our [Huggingface Datasets](https://huggingface.co/datasets/dennlinger/klexikon) version for easy access of the preprocessed data.


## Installation

This repository contains the code to crawl the Klexikon data set presented in our paper,
as well as all associated baselines and splits.
You can work on the existing code base by simply cloning this repository.

Install all required dependencies with the following command:
```bash
python3 -m pip install -r requirements.txt
```
The experiments were run on Python 3.8.4, but should run fine with any version >3.7.
To run files, relative imports are required, which forces you to run them as modules, e.g.,

```bash
python3 -m klexikon.analysis.compare_offline_stats
```
instead of
```bash
python3 klexikon/analysis/compare_offline_stats.py
```
Furthermore, this requires the working directory to be the root folder as well,
to ensure correct referencing of relative data paths.
I.e., if you cloned this repository into `/home/dennis/projects/klexikon`,
make sure to run scripts directly from this path.

## Extended Explanation
### Manually Replaced Articles in `articles.json`
Aside from all the manual matches, which can be produced by `create_matching_url_list.py`,
there are some articles which simply link to an incorrect article in Wikipedia.  
We approximate this by the number of paragraphs in the Wikipedia article, 
which is generally much longer than the Klexikon article, and therefore should have at least 15 paragraphs.
Note that most of the pages are disambiguations, which unfortunately don't necessarily
correspond neatly to a singular Wikipedia page. We remove the article if it is not possible to find a singular Wikipedia article
that covers more than 66% of the paragraphs in the Klexikon article.
Some examples for manual changes were:

* "Aal" to "Aale"
* "Abendmahl" to "Abendmahl Jesu"
* "Achse" to "Längsachse"
* "Ader" to "Blutgefäß"
* "Albino" to "Albinismus"
* "Alkohol" to "Ethanol"
* "Android" to "Android (Betriebssystem)"
* "Anschrift" to "Postanschrift"
* "Apfel" to "Kulturapfel"
* "App" to "Mobile App"
* "Appenzell" to "Appenzellerland"
* "Arabien" to "Arabische Halbinsel"
* "Atlas" to "Atlas (Kartografie)"
* "Atmosphäre" to "Erdatmospähre"


### Merging sentences that end in a semicolon (`;`)
This applies to any position in the document. The reason is rectifying some unwanted splits by spaCy.

### Merge of short lines in lead 3 baseline
Also checking for lines that have less than 10 characters in the first three sentences.
This helps with fixing the lead-3 baseline, and most issues arise from some incorrect splits to begin with.

### Removal of coordinates
Sometimes, coordinate information is leading in the data, which seems to be embedded in some Wikipedia articles.
We remove any coordinate with a simple regex.

### Sentences that do not end in a period
Manual correction of sentences (in the lead 3) that do not end in periods.
This has been automatically fixed by merging content similarly to the semicolon case.
Specifically, we only merge if the subsequent line is *not* just an empty line.

## Using your own data
Currently, the systems expect input data to be processed in a line-by-line fashion,
where every line represents a sentence, and each file represents an input document.
Note that we currently do not support multi-document summarization.

## Criteria for discarding articles
Articles where Wikipedia has less than 15 paragraphs.
Otherwise, manually discarding when there are no matching articles in Wikipedia (see above).
Examples of the latter case are for example "Kiwi" or "Washington"

## Reasons for not using lists
As described in the paper, we discard any element that is not a `<p>` tag in the HTLM code.
This helps getting rid of actual unwanted information (images, image captions, meta-descriptors, etc.),
but also removes list items. After reviewing some examples, we have decided to discard list elements altogether.
This means that some articles (especially disambiguation pages) are also easier to detect.

# Final number of valid article pairs: 2898
This means we had to discard around 250 articles from the original list at the time of crawling (April 2021).
In the meantime, there have been new articles added to Klexikon, which leaves room for future improvements.

# Execution Order of Scripts
TK: I'll include a better reference to the particular scripts in the near future, as well as a script that actually executes everything relevant in order.

* Generate JSON file with article URLs
* Crawl texts
* Fix lead sentences
* Remove unused articles (optional)
* Generate stratified split

# License Information
Both Wikipedia and Klexikon make their textual contents available under the CC BY-SA license.
Per [recommendation of the Creative Commons](https://creativecommons.org/faq/#can-i-apply-a-creative-commons-license-to-software), we apply a separate license to the software component of this repository.
Data will be re-distributed under the CC BY-SA license.

# Contributions
Contributions are very welcome. Please either open an issue or pull request if you have any suggestion on how this data can be improved.
Open TODOs:

* So far, the data does not have more than a few simplistic baselines, and lacks an actually trained system on top of the data.
* The dataset is "out-of-date", since it does not include any of the more recently articles (~100 since the inception of my version). Potentially, we can increase the availability to almost 3000 articles.
* Adding a top-level script that adds correct execution order of different scripts to generate baselines/results/etc.
* Adding a proper data managing script for the Huggingface Datasets version of this dataset.

# How to Cite?
If you use our dataset, or code from this repository, please cite our LREC'22 paper:
```bibtex
@inproceedings{aumiller-gertz-2022-klexikon,
    title = "Klexikon: A {G}erman Dataset for Joint Summarization and Simplification",
    author = "Aumiller, Dennis  and
      Gertz, Michael",
    booktitle = "Proceedings of the Thirteenth Language Resources and Evaluation Conference",
    month = jun,
    year = "2022",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://aclanthology.org/2022.lrec-1.288",
    pages = "2693--2701"
}
```
