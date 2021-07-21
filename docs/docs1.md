
# corpus-toolkit Documentation Page
This page includes details on the arguments each function in the corpus-toolkit package takes.

**Note that this page is in progress!** All (heavily commented) code is [also available here](https://github.com/kristopherkyle/corpus_toolkit/blob/master/corpus_toolkit/corpus_tools.py)

## Default lists

```python
default_punct_list = [",",".","?","'",'"',"!",":",";","(",")","[","]","''","``","--"] #we can add more items to this if needed
default_space_list = ["\n","\t","    ","   ","  "]
```

## ldcorpus()

This function will load all files that match a certain filename ending (e.g., ".txt") in a folder. By default it loads all files ending in ".txt" and prints the name of each file being loaded.

**ldcorpus()** Is a generator function that loads all corpus files in a folder. It takes three arguments (two of which have default values):
- **dirname** (*string variable*) This is the name of the directory that one's files are in. It will not gather files in nested folders.
- **ending** (*string variable*) This is the ending for your target filenames. By default, this is ".txt".
- **verbose** (*Boolean variable*) This determines whether filenames are printed to the console when loading. By default, this is set to "True"

```python
def ldcorpus(dirname,ending = ".txt",verbose = True):
		filenames = glob.glob(dirname + "/*" + ending) #gather all text names
		nfiles = len(filenames) #get total number of files in corpus
		fcount = 0 #counter for corpus files
		for x in filenames:
			fcount +=1 #update file count
			sm_fname = x.split(dirsep)[-1] # get filename
			if verbose == True:
				print("Processing", sm_fname, "(" + str(fcount), "of", nfiles,"files)")
			text = open(x, errors = "ignore").read()
			yield(text)
```
## tokenize()

**tokenize()** Is a generator function that tokenizes a list of texts. It takes eight arguments (seven of which have default values):
- **corpus** (*list of texts*) This is a list of corpus texts (strings)
- **remove_list** (*list of characters*) This is a list of characters to be removed from each text. By default this is the `default_punct_list`
- **space_list** (*list of characters*) This is a list of characters (and character sequences) to be replaced by a single space. By default this is the `default_space_list`
- **split_token** (*string variable*) This is the character used to split the text string. By default this is a single space ```python " " ```.
- **lower** (*Boolean variable*) This is a Boolean value that determines whether all characters in each text are set to lower case. By default, this is true.
- **lemma** (*dictionary*) This is the lemma dictionary used to lemmatize tokens in each text that consists of lower-case unlemmatized words as keys and lemmas as values. By default, this is a pre-loaded lemma list. If set to False, then texts are not lemmatized.
- **ngram** (*Boolean variable or integer*) This sets the n-gram length for tokenization. By default, this is set to False.
- **ngrm-connect** (*string variable*) This sets the character used to join words in an ngram. By default, this is set to `"__"`

```python
def tokenize(corpus, remove_list = default_punct_list, space_list = default_space_list, split_token = " ", lower = True, lemma=lemma_dict,ngram = False,ngrm_connect = "__"):
	for text in corpus: #iterate through each string in the corpus_list
		for item in remove_list:
			text = text.replace(item,"") #replace each item in list with "" (i.e., nothing)
		for item in space_list:
			text = text.replace(item," ")
		if lower == True:
			text = text.lower()
		#then we will tokenize the document
		tokenized = text.split(split_token) #split string into list using the split token (by default this is a space " ")
		if lemma != False: #if lemma isn't False
			tokenized = lemmatize(tokenized,lemma)
		if ngram != False:
			tokenized = ngrammer(tokenized,ngram,ngrm_connect)

		yield(tokenized)
```
