
## Default lists

```python
default_punct_list = [",",".","?","'",'"',"!",":",";","(",")","[","]","''","``","--"] #we can add more items to this if needed
default_space_list = ["\n","\t","    ","   ","  "]
```

## Load corpus

This function will load all files that match a certain filename ending (e.g., ".txt") in a folder. By default it loads all files ending in ".txt" and prints the name of each file being loaded.

**ldcorpus()** Is a generator function that loads all corpus files in a folder. It takes three arguments (two of which have default values):
- **dirname** (*string variable*) This is the name of the directory that one's files are in. It will not gather files in nested folders.
- **ending** (*string variable*) This is the ending for your target filenames. By default, this is ".txt".
- **verbose** (*Boolean variable*) This determines whether filenames are printed to the console when loading. By default, this is set to "True"

## tokenize corpus

**tokenize()** Is a generator function that tokenizes a list of texts. It takes eight arguments (seven of which have default values):
- **corpus** (*list of texts*) This is a list of corpus texts (strings)
- **remove_list** (*list of characters*) This is a list of characters to be removed from each text. By default this is the `default_punct_list`
- **space_list** (*list of characters*) This is a list of characters (and character sequences) to be replaced by a single space. By default this is the `default_space_list`
- **split_token** (*string variable*) This is the character used to split the text string. By default this is a single space ```python " " ```.
- **lower** (*Boolean variable*) This is a Boolean value that determines whether all characters in each text are set to lower case. By default, this is true.
- **lemma** (*dictionary*) This is the lemma dictionary used to lemmatize tokens in each text that consists of lower-case unlemmatized words as keys and lemmas as values. By default, this is a pre-loaded lemma list. If set to False, then texts are not lemmatized.
- **ngram** (*Boolean variable or integer*) This sets the n-gram length for tokenization. By default, this is set to False.
- **ngrm-connect** (*string variable*) This sets the character used to join words in an ngram. By default, this is set to ```python "__" ```
