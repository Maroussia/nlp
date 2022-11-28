# Why ReadITI

ReadITI is designed to prepare texts from the OpenITI corpus for Natural Language Processing. You can download OpenITI at [Zenodo](https://doi.org/10.5281/zenodo.6808108). If you use it, be sure to cite

 > Nigst, Lorenz, Romanov, Maxim, Savant, Sarah Bowen, Seydi, Masoumeh, & Verkinderen, Peter. (2022). OpenITI: a Machine-Readable Corpus of Islamicate Texts (2022.1.6) [Data set]. Zenodo. 


ReadITI is inspired from [`openiti.helper.ara`](
https://openiti.readthedocs.io/en/latest/source/usermanual.html#openiti-helper).

ReadITI separates the metadata and cuts the text into sentences or paragraphs using the OpenITI hashtags (#), whereas `openiti.helper.ara.tokenize` preserves metadata so that it will appear in your tokenized input.


# Using ReadITI

The function `readiti.file_processor` processes single files and is meant for scholars working with one version of a given text.

The function `readiti.dir_preprocessor` processes all the files in a directory and is addressed to scholars who have extracted a corpus with multiple texts. Set `verbose=False` if to prevent the printing of statistics during preprocessing (default `verbose=True`).

The **input** for both functions should be raw files from OpenITI.

The **output** for both functions consists in 3 files per input file. Output file names are the original OpenITI name `<name>` with a suffix: followed by a swith a suffix tokens (1), sentences (2) or doc (3) is added at the end.

1. a `<name>.txt_tokens.txt` file containing one *token* per line resulting from simple white-space tokenization.
	
2. a `<name>.txt_sentences.txt` file containing one OpenITI *sentence* per line. The end of a sentence corresponds to a new line in the original text, which OpenITI marks with a hastag (#). Hence you can cut up sentences in the input by inserting # at the desired sites.
	
3. a `<name>.txt_doc.tsv` table where the tab (`\t`)-separated columns contain: 

```
token id (index into the vocabulary), token characters, index of the starting character index, index of ending character.
```


Sentences in all files are separated by two new lines (`\n\n`).


See the folder `readiti/data/trial_with_folder/output` for examples.

Anything missing? Do get in touch or open up a pull request :).
