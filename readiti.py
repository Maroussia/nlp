###################################################################
# Customised OpenITI Text Preprocessing | by Maroussia Bednarkiewicz
###################################################################

import os
import re
import pandas as pd
from itertools import chain

###################################################################
# Get the text content of a file
###################################################################

def get_content(fname: str) -> tuple:
    """Return OpenITI metadata and content separately.

    Return a tuple of two strings containing
    (1) the metadata;
    (2) the text content in Arabic.
    """
    
    with open(fname, 'r+') as wrapper:
        text_all = wrapper.read()
        
        # META section ends with #META#Header#End# and two newlines
        meta, _, text = text_all.partition('#META#Header#End#\n\n')
    
    return meta, text

###################################################################
# Clean the text content to retain only the Arabic and separator
###################################################################

def cleaner(text: str) -> list[str]:
    """Return a list of all the Arabic tokens and the sentence separators.
    """
    # Note this regex preserves hashtags, which mark sentence boundaries
    arabic_regex = "[ذ١٢٣٤٥٦٧٨٩٠ّـضصثقفغعهخحجدًٌَُلإإشسيبلاتنمكطٍِلأأـئءؤرلاىةوزظْلآآ]+|#+"
    
    tokens = (m for m in re.finditer(arabic_regex, text))
    
    return [m.group() for m in tokens]

###################################################################
# Break the text into sentences
###################################################################

def sentencizer(cleaned: list[str]) -> list[str]:
    """Return a list of sentences from the list of tokens.
    """

    text_str = ' '.join(cleaned)

    return [s for s in text_str.split('#') if len(s) > 0]

###################################################################
# Generate a customized doc object
###################################################################

def indexizer(sentences: list[str]) -> list[str]:
    """Return a list of sentences which contain each a list of dictionaries
    with token_idx, token, start_chr, end_chr for each token of the sentence.
    """

    char_idx = 0
    document = []

    for sentence in sentences:
        token_spans = []
        for token_idx, token in enumerate(sentence.split()):
            token_len = len(token)
            token_spans.append(dict(token_idx=token_idx,
                                    token=token,
                                    start_char=char_idx,
                                    end_char=char_idx+token_len))
            char_idx += token_len + 1
        document.append(token_spans)
    return document

###################################################################
# General functions
###################################################################

def file_processor(src_file: str, dst_dir: str, verbose=True) -> None:
    """Generate three files from src_file:
    (1) tokens.txt with the Arabic tokens of src_file;
    (2) sentences.txt with the Arabic tokens grouped by sentences;
    (3) doc.tsv with for each token, its index in the sentence 
    and character span (start and end), the function indexizer creates 
    a list of list of dictionaries as the example below shows which it
    then converts into a tsv file with the keys as column names:

    indexizer output:
    [[{'idx': 0, 'token': 'ذكر', 'start_char': 0, 'end_char': 3},
      {'idx': 1, 'token': 'من', 'start_char': 4, 'end_char': 6},
      {'idx': 2, 'token': 'حدث', 'start_char': 7, 'end_char': 10}], ...]

    The output files are stored in dst_dir.
    Verbose prints the length of src_file, the number of tokens, and
    the number of sentences.
    """

    _, text = get_content(src_file)
    cleaned = cleaner(text)
    sentences = sentencizer(cleaned)
    indexed = indexizer(sentences)

    with open(os.path.join(dst_dir, 'tokens.txt'), 'w') as new_file:
        # Convert hashtags into newlines to mark sentence boundaries
        out = '\n'.join(cleaned).replace('#', '')
        new_file.write(re.sub('\n{3,}', '\n\n', out))
    
    with open(os.path.join(dst_dir, 'sentences.txt'), 'w') as new_file:
        new_file.write('\n'.join(sentences))

    df_indexed = pd.DataFrame(list(chain.from_iterable(indexed)))
    df_indexed.to_csv(os.path.join(dst_dir, 'doc.tsv'), sep="\t")
    
    if verbose:
        print(f"length original: {len(text.split())}")
        print(f"number of sentences: {len(sentences)}")
        count_new_line = cleaned.count('\n\n')
        print(f"number of tokens: {len(cleaned) - count_new_line}")


def dir_processor(src_dir: str, dst_dir: str, verbose=True) -> None:
    """Generate three files from each file in src_dir:
    (1) fname_tokens.txt with the Arabic tokens of src_file;
    (2) fname_sentences.txt with the Arabic tokens grouped by sentences;
    (3) fname_doc.tsv with for each token its index in the sentence 
    and character span (start and end), the function indexizer creates 
    a list of list of dictionaries as the example below shows which it
    then converts into a tsv file with the keys as column names:

    indexizer output:
    [[{'idx': 0, 'token': 'ذكر', 'start_char': 0, 'end_char': 3},
      {'idx': 1, 'token': 'من', 'start_char': 4, 'end_char': 6},
      {'idx': 2, 'token': 'حدث', 'start_char': 7, 'end_char': 10}], ...]

    The output files are stored in dst_dir.
    Verbose prints the length of src_file, the number of tokens, and
    the number of sentences.
    """

    for root, dirs, files in os.walk(src_dir, topdown=False):
        for name in files:
            _, text = get_content(os.path.join(root, name))
            cleaned = cleaner(text)
            sentences = sentencizer(cleaned)
            indexed = indexizer(sentences)
            
            if verbose:
                print(name)
                print(f"length original: {len(text.split())}")
                print(f"number of sentences: {len(sentences)}")
                count_new_line = cleaned.count('\n\n')
                print(f"number of tokens: {len(cleaned) - count_new_line}")

            with open(os.path.join(dst_dir, name + '_tokens.txt'), 'w') as new_file:
                # Convert hashtags into newlines to mark sentence boundaries
                out = '\n'.join(cleaned).replace('#', '')
                new_file.write(re.sub('\n{3,}', '\n\n', out))
            
            with open(os.path.join(dst_dir, name + '_sentences.txt'), 'w') as new_file:
                new_file.write('\n'.join(sentences))

            df_indexed = pd.DataFrame(list(chain.from_iterable(indexed)))
            df_indexed.to_csv(os.path.join(dst_dir, name + '_doc.tsv'), sep="\t")

