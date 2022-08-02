ReadITI is designed to clean texts from the OpenITI corpus and prepare them for Natural Language Processing (tasks).
It is inspired from `openiti.helper.ara`:
https://openiti.readthedocs.io/en/latest/source/usermanual.html#openiti-helper
If you use `openiti.helper.ara.tokenize` to clean your text(s) from annotations and tokenize it, bear in mind that the Arabic metadata will be preserved and appear as tokens in your output. ReadITI allows you to separate the metadata and cut the text into sentences or paragraphs using the hashtags (#).

You can download OpenITI on the zenodo platform:
https://doi.org/10.5281/zenodo.6808108

To credit its authors you should use the following citation:
Nigst, Lorenz, Romanov, Maxim, Savant, Sarah Bowen, Seydi, Masoumeh, & Verkinderen, Peter. (2022). OpenITI: a Machine-Readable Corpus of Islamicate Texts (2022.1.6) [Data set]. Zenodo. 

User Guide for ReadITI:

`readiti.file_processor` processes single files and is meant for scholars working with one version of a given text.

`readiti.dir_preprocessor` processes all the files in a directory and is addressed to scholars who have extracted a corpus with multiple texts. Set verbose=False if you do not want to have statistics about your texts being printed out (default verbose=True).

The **input** for both functions should be raw files from OpenITI.

The **output** for both functions consists in 3 files [for each file]:
1. a file in .txt with each line containing one token followed by a new line ('\n'). The function uses a simple white-space tokenization.
2. a file in .txt with each line containing a sentence. The end of a sentence corresponds to a new line in the original text, which OpenITI marks with a hastag (#). You can add hashtags if you want to increase the amount of sentences.
3. a file in .tsv with a list of dictionaries that each contains the token ids, the token, the starting character index and the ending character index separated by tabs ('\t').

Sentences in all files are separate by two new lines ('\n\n').

The name of the original OpenITI file is preserved and tokens (1), sentences (2) or doc (3) is added at the end.

See the folder /readiti/data/trial_with_folder/output/ for examples.

Anything missing? Do get in touch or make suggestions :)