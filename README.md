# Corpus-toolkit
The corpus-toolkit package grew out of courses in corpus linguistics and learner corpus research. The toolkit attempts to balance simplicity of use, broad application, and scalability. Common corpus analyses such as the calculation of word and n-gram frequency and range, keyness, and collocation are included. In addition, more advanced analyses such as the identification of dependency bigrams (e.g., verb-direct object combinations) and their frequency, range, and strength of association are also included.

More details on each function in the package (including various option settings) can be found on the [corpus-toolkit resource page](docs/docs1.md).
## Install corpus-toolkit
The package can be downloaded using pip
```bash
pip install corpus-toolkit
```
### Dependencies
The corpus-toolkit package makes use of Spacy for tagging and parsing. However, the package also includes a tokenization and lemmatization function that does not require Spacy. If you want to tag or parse your files, you will need to [install Spacy](https://spacy.io/usage) (and an appropriate [Spacy language model](https://spacy.io/usage/models#quickstart)).
```bash
pip install -U spacy
python -m spacy download en_core_web_sm
```
## Quickstart guide
There are three corpus pre-processing options. The first is to use the **tokenize()** function, which does not rely on a part of speech tagger. The second is to use the **tag()** function, which uses [Spacy](https://spacy.io/) to tokenize and tag the corpus. The third option is to pre-process the corpus in any way you like before using the other functions of the corpus-toolkit package.

This tutorial presumes that you have downloaded and extracted the [brown_single.zip](https://github.com/kristopherkyle/Corpus-Methods-Intro/blob/master/Course-Materials/brown_single.zip?raw=true), which is a version of the [Brown corpus](http://clu.uni.no/icame/manuals/BROWN/INDEX.HTM). The folder "brown_single" should be in your working directory.

### Load, tokenize, and generate a frequency list

```python
from corpus_toolkit import corpus_tools as ct
brown_corp = ct.ldcorpus("brown_single") #load and read corpus
tok_corp = ct.tokenize(brown_corp) #tokenize corpus - by default this lemmatizes as well
brown_freq = ct.frequency(tok_corp) #creates a frequency dictionary
#note that range can be calculated instead of frequency using the argument calc = "range"
ct.head(brown_freq, hits = 10) #print top 10 items

```
```
the     69836
be      37689
of      36365
a       30475
and     28826
to      26126
in      21318
he      19417
have    11938
it      10932
```
The functions **ldcorpus()** and **tokenize()** are [Python generators](https://wiki.python.org/moin/Generators), which means that they must be re-declared each time they are used (iterated over). A slightly messier (but more appropriate) way to achieve the results above is to nest the commands.
```python
brown_freq = ct.frequency(ct.tokenize(ct.ldcorpus("brown_single")))
ct.head(brown_freq, hits = 10)
```
```
the     69836
be      37689
of      36365
a       30475
and     28826
to      26126
in      21318
he      19417
have    11938
it      10932
```

Note that the **frequency()** function can also calculate range and normalized frequency figures. See the [resource page](docs/docs1.md) for details.

### Generate concordance lines
Concordance lines can be generated using the **concord()** function. By default, a random sample of 25 hits will be generated, with 10 tokens of left and right context.

```python
conc_results1 = ct.concord(ct.tokenize(ct.ldcorpus("brown_single"),lemma = False),["run","ran","running","runs"],nhits = 10)
for x in conc_results1:
	print(x)
```

```
[['buckle', 'drag', 'the', 'wagons', 'to', 'the', 'spring', 'lew', 'durkin', 'yelled'], 'run', ['em', 'right', 'into', 'the', 'spring', 'hustle', 'one', 'of', 'the', 'wagons']]
[['his', 'sweater', 'soaking', 'into', 'a', 'dark', 'streak', 'of', 'dirt', 'that'], 'ran', ['diagonally', 'across', 'the', 'white', 'wool', 'on', 'his', 'shoulder', 'as', 'though']]
[['took', 'a', 'hasty', 'shot', 'then', 'fled', 'without', 'knowing', 'the', 'result'], 'ran', ['until', 'breath', 'was', 'a', 'pain', 'in', 'his', 'chest', 'and', 'his']]
[['back', 'to', 'new', 'york', 'as', 'maude', 'suggested', 'she', 'would', 'nt'], 'run', ['like', 'a', 'scared', 'cat', 'but', 'well', 'she', 'd', 'be', 'very']]
[['with', 'that', 'soap', 'i', 'was', 'loaded', 'with', 'suds', 'when', 'i'], 'ran', ['away', 'and', 'i', 'have', 'nt', 'had', 'a', 'chance', 'to', 'wash']]
[['conditions', 'of', 'international', 'law', 'are', 'met', 'countries', 'that', 'try', 'to'], 'run', ['the', 'blockade', 'do', 'so', 'at', 'their', 'own', 'risk', 'blockade', 'runners']]
[['produce', 'something', 'which', 'has', 'not', 'previously', 'existed', 'thus', 'creativity', 'may'], 'run', ['all', 'the', 'way', 'from', 'making', 'a', 'cake', 'building', 'a', 'chicken']]
[['from', 'the', 'school', 'he', 'did', 'nt', 'look', 'back', 'and', 'he'], 'ran', ['until', 'he', 'was', 'out', 'of', 'sight', 'of', 'the', 'schoolhouse', 'and']]
[['in', 'my', 'body', 'i', 'could', 'light', 'all', 'the', 'lights', 'and'], 'run', ['all', 'the', 'factories', 'in', 'the', 'entire', 'united', 'states', 'for', 'some']]
[['in', 'any', 'time', 'they', 'please', 'sergeant', 'no', 'sir', 'running', 'in'], 'running', ['out', 'ca', 'nt', 'have', 'it', 'makes', 'for', 'confusion', 'and', 'congestion']]
```

Collocates can also be added as secondary search terms:

```python
conc_results2 = ct.concord(ct.tokenize(ct.ldcorpus("brown_single"),lemma = False),["run","ran","running","runs"],collocates = ["quick","quickly"], nhits = 10)
for x in conc_results2:
	print(x)
```

```
[['range', 'and', 'in', 'marlin', 's', 'underground', 'test', 'gallery', 'we', 'quickly'], 'ran', ['into', 'the', 'same', 'trouble', 'that', 'plagued', 'bill', 'ruger', 'in', 'his']]
[['s', 'nest', 'to', 'the', 'rocky', 'ribs', 'of', 'the', 'canyonside', 'russ'], 'ran', ['up', 'the', 'steps', 'quickly', 'to', 'the', 'plank', 'porch', 'the', 'front']]
[['hands', 'and', 'feet', 'keeping', 'the', 'hands', 'in', 'the', 'starting', 'position'], 'run', ['in', 'place', 'to', 'a', 'quick', 'rhythm', 'after', 'this', 'has', 'become']]
[['engine', 'up', 'to', 'operating', 'temperature', 'quickly', 'and', 'to', 'keep', 'it'], 'running', ['at', 'its', 'most', 'efficient', 'temperature', 'through', 'the', 'proper', 'circulation', 'of']]
```

Search terms (and collocate search terms) can also be interpreted as regular expressions:
```python
conc_results3 = ct.concord(ct.tokenize(ct.ldcorpus("brown_single"),lemma = False),["run.*","ran"],collocates = ["quick.*"], nhits = 10, regex = True)
for x in conc_results3:
	print(x)
```

```
[['impact', 'we', 'fired', 'this', 'little', '20-inch-barrel', 'job', 'on', 'my', 'home'], 'range', ['and', 'in', 'marlin', 's', 'underground', 'test', 'gallery', 'we', 'quickly', 'ran']]
[['range', 'and', 'in', 'marlin', 's', 'underground', 'test', 'gallery', 'we', 'quickly'], 'ran', ['into', 'the', 'same', 'trouble', 'that', 'plagued', 'bill', 'ruger', 'in', 'his']]
[['minutes', 'the', 'gallery', 'leaders', 'had', 'given', 'the', 'students', 'a', 'quick'], 'rundown', ['on', 'art', 'from', 'the', 'renaissance', 'to', 'the', 'late', '19th', 'century']]
[['s', 'nest', 'to', 'the', 'rocky', 'ribs', 'of', 'the', 'canyonside', 'russ'], 'ran', ['up', 'the', 'steps', 'quickly', 'to', 'the', 'plank', 'porch', 'the', 'front']]
[['hands', 'and', 'feet', 'keeping', 'the', 'hands', 'in', 'the', 'starting', 'position'], 'run', ['in', 'place', 'to', 'a', 'quick', 'rhythm', 'after', 'this', 'has', 'become']]
[['engine', 'up', 'to', 'operating', 'temperature', 'quickly', 'and', 'to', 'keep', 'it'], 'running', ['at', 'its', 'most', 'efficient', 'temperature', 'through', 'the', 'proper', 'circulation', 'of']]
```

Concordance lines can also be written to a file for easier analysis (e.g., using spreadsheet software). By default, items are separated by tab characters ("\t").

```python
#write concordance lines to a file called "run_25.txt"
conc_results4 = ct.concord(ct.tokenize(ct.ldcorpus("brown_single"),lemma = False),["run","ran","running","runs"], outname = "run_25.txt")
```


### Create a tagged version of your corpus

The most efficient way to conduct multiple analyses with a tagged corpus is to write a tagged version of your corpus to file and then conduct subsequent analyses with the tagged files. If this is not possible for some reason, one can always run the tagger each time an analysis is conducted.

```python
tagged_brown = ct.tag(ct.ldcorpus("brown_single"))
ct.write_corpus("tagged_brown_single",tagged_brown) #the first argument is the folder where the tagged files will be written
```
The function **tag()** is also a Python generator, so the preferred way to write a corpus is:
```python
ct.write_corpus("tagged_brown_single",ct.tag(ct.ldcorpus("brown_single")))
```

Now, we can reload our tagged corpus using the **reload()** function and generate a part of speech sensitive frequency list.

```python
tagged_freq = ct.frequency(ct.reload("tagged_brown_single"))
ct.head(tagged_freq, hits = 10)
```
```
the_DET 69861
be_VERB 37800
of_ADP  36322
and_CCONJ       28889
a_DET   23069
in_ADP  20967
to_PART 15409
have_VERB       11978
to_ADP  10800
he_PRON 9801
```
## Collocation

Use the **collocator()** function to find collocates for a particular word.

```Python
collocates = ct.collocator(ct.tokenize(ct.ldcorpus("brown_single")),"go",stat = "MI")
#stat options include: "MI", "T", "freq", "left", and "right"

ct.head(collocates, hits = 10)
```
```
downstairs      7.875170389265524
upstairs        6.915812373762869
bedroom 6.627242875821938
abroad  6.273134375185426
re      6.21620730710059
m       6.211322724303333
forever 6.174730671124432
stanley 6.174730671124432
let     5.938347287580174
wrong   5.868744120106091
```

## Keyness
Keyness is calculated using two frequency dictionaries (consisting of raw frequency values). Only effect sizes are reported (_p_ values are arguably not particularly useful for keyness analyses). Keyness calculation options include "log-ratio", "%diff", and "odds-ratio".

```python
#First, generate frequency lists for each corpus
corp1freq = ct.frequency(ct.tokenize(ct.ldcorpus("corp1")))
corp2freq = ct.frequency(ct.tokenize(ct.ldcorpus("corp2")))

#then calculate Keyness
corp_key = ct.keyness(corp1freq,corp2freq, effect = "log-ratio")
ct.head(corp_key, hits = 10) #to display top hits
```
## N-grams

N-grams are contiguous sequences of _n_ words. The **tokenize()** function can be used to create an n-gram version of a corpus by employing the **ngram** argument. By default, words in an n-gram are separated by two underscores "\_\_"

```Python
trigramfreq = ct.frequency(ct.tokenize(ct.ldcorpus("brown_single"),lemma = False, ngram = 3))
ct.head(trigramfreq, hits = 10)
```
```
one__of__the    404
the__united__states     339
as__well__as    237
some__of__the   179
out__of__the    172
the__fact__that 167
i__do__nt       162
the__end__of    149
part__of__the   144
it__was__a      143
```

## Dependency bigrams
Dependency bigrams consist of two words that are syntactically connected via a head-dependent relationship. For example, in the clause "The player **_kicked_** the **_ball_**", the main verb **_kicked_** is connected to the noun **_ball_** via a direct object relationship, wherein **_kicked_** is the head and **_ball_** is the dependent.

The function **dep_bigram()** generates frequency dictionaries for the dependent, the head, and the dependency bigram. In addition, range is calculated along with a complete list of sentences in which the relationship occurs.

```Python
bg_dict = ct.dep_bigram(ct.ldcorpus("brown_single"),"dobj")
ct.head(bg_dict["bi_freq"], hits = 10)
#other keys include "dep_freq", "head_freq", and "range"
#also note that the key "samples" can be used to obtain a list of sample sentences
#but, this is not compatible with the ct.head() function (see ct.dep_conc() instead)
```
```
#all dependency bigrams are formatted as dependent_head
what_do 247
place_take      84
what_say        80
him_told        67
it_do   63
that_do 51
time_have       49
what_mean       46
this_do 46
what_call       42
```

### Strength of association

Various measures of strength of association can calculated between dependents and heads. The **_soa()_** function takes a dictionary generated by the **_dep_bigram()_** function and calculates the strength of association for each dependency bigram.

```Python
soa_mi = ct.soa(bg_dict,stat = "MI")
#other stat options include: "T", "faith_dep", "faith_head","dp_dep", and "dp_head"
ct.head(soa_mi, hits = 10)
```
```
radiation_ionize        12.037110123486007
B_paragraph     12.037110123486007
suicide_commit  10.648544835568353
nose_scratch    10.39700606857239
calendar_adjust 9.972979786066292
imagination_capture     9.774075717652213
nose_blow       9.672113306706759
English_speak   9.496541742123304
throat_clear    9.367258725178337
expense_deduct  9.256227412789594
```
### Concordance lines for dependency bigrams
A number of excellent cross-platform GUI- based concordancers such as [AntConc](https://www.laurenceanthony.net/software/antconc/) are freely available, and are likely the preferred method for most concordancing.

However, it is difficult to get concordance lines for dependency bigrams without a more advanced program. The **_dep_conc()_** function takes the samples generated by the **_dep_bigram()_** function and creates a random sample of hits (50 hits by default) formatted as an html file.

The following example will write an html file named "dobj_results.html" to your working directory.

```python
ct.dep_conc(bg_dict["samples"],"dobj_results")
```
When opened, the resulting file will include the following:

<html><head><style>dep {color:red;}
 dep_head {color:blue;}</style></head><p><word>A </word><word>fringe </word><word>of </word><word>housing </word><word>and </word><word>gardens </word><dep_head>bearded_dobj_head </dep_head><word>the </word><dep>top_dobj_dep </dep><word>of </word><word>the </word><word>heights </word><word>, </word><word>and </word><word>behind </word><word>it </word><word>were </word><word>sandy </word><word>roads </word><word>leading </word><word>past </word><word>farms </word><word>and </word><word>hayfields </word><word>. </word><word>
 </word><word>39 </word></p><p><word>A </word><word>man </word><word>with </word><word>insomnia </word><word>had </word><word>better </word><dep_head>avoid_dobj_head </dep_head><word>bad </word><dep>dreams_dobj_dep </dep><word>of </word><word>that </word><word>kind </word><word>if </word><word>he </word><word>knew </word><word>what </word><word>was </word><word>good </word><word>for </word><word>him </word><word>. </word><word>
 </word><word>241 </word></p><p><word>He </word><word>simply </word><word>would </word><word>not </word><dep_head>work_dobj_head </dep_head><word>his </word><word>arithmetic </word><dep>problems_dobj_dep </dep><word>when </word><word>the </word><word>teacher </word><word>held </word><word>his </word><word>class </word><word>. </word><word>
 </word><word>192 </word></p><p><word>You </word><word>may </word><word>be </word><word>sure </word><word>he </word><word>marries </word><word>her </word><word>in </word><word>the </word><word>end </word><word>and </word><dep_head>has_dobj_head </dep_head><word>a </word><word>fine </word><word>old </word><word>knockdown </word><dep>fight_dobj_dep </dep><word>with </word><word>the </word><word>brother </word><word>, </word><word>and </word><word>that </word><word>there </word><word>are </word><word>plenty </word><word>of </word><word>minor </word><word>scraps </word><word>along </word><word>the </word><word>way </word><word>to </word><word>ensure </word><word>that </word><word>you </word><word>understand </word><word>what </word><word>the </word><word>word </word><word>Donnybrook </word><word>means </word><word>. </word><word>
 </word><word>198 </word></p><p><word>Anyone </word><word>familiar </word><word>with </word><word>the </word><word>details </word><word>of </word><word>the </word><word>McClellan </word><word>hearings </word><word>must </word><word>at </word><word>once </word><word>realize </word><word>that </word><word>the </word><word>sweetheart </word><word>arrangements </word><dep_head>augmented_dobj_head </dep_head><word>employer </word><dep>profits_dobj_dep </dep><word>far </word><word>more </word><word>than </word><word>they </word><word>augmented </word><word>the </word><word>earnings </word><word>of </word><word>the </word><word>corruptible </word><word>labor </word><word>leaders </word><word>. </word><word>
 </word><word>407 </word></p><p><word>If </word><word>the </word><word>transferor </word><dep_head>has_dobj_head </dep_head><word>substantial </word><dep>assets_dobj_dep </dep><word>other </word><word>than </word><word>the </word><word>claim </word><word>, </word><word>it </word><word>seems </word><word>reasonable </word><word>to </word><word>assume </word><word>no </word><word>corporation </word><word>would </word><word>be </word><word>willing </word><word>to </word><word>acquire </word><word>all </word><word>of </word><word>its </word><word>properties </word><word>in </word><word>the </word><word>dim </word><word>hope </word><word>of </word><word>collecting </word><word>a </word><word>claim </word><word>for </word><word>refund </word><word>of </word><word>taxes </word><word>. </word><word>
 </word><word>433 </word></p><p><word>For </word><word>the </word><word>first </word><word>few </word><word>months </word><word>of </word><word>their </word><word>marriage </word><word>she </word><word>had </word><word>tried </word><word>to </word><word>be </word><word>nice </word><word>about </word><word>Gunny </word><word>, </word><word>going </word><word>out </word><word>with </word><word>him </word><word>to </word><dep_head>watch_dobj_head </dep_head><word>this </word><dep>pearl_dobj_dep </dep><word>without </word><word>price </word><word>stamp </word><word>imperiously </word><word>around </word><word>in </word><word>her </word><word>stall </word><word>. </word><word>
 </word><word>441 </word></p><p><word>If </word><word>the </word><word>site </word><word>is </word><word>on </word><word>a </word><word>reservoir </word><word>, </word><word>the </word><word>level </word><word>of </word><word>the </word><word>water </word><word>at </word><word>various </word><word>seasons </word><word>as </word><word>it </word><dep_head>affects_dobj_head </dep_head><dep>recreation_dobj_dep </dep><word>should </word><word>be </word><word>studied </word><word>. </word><word>
 </word><word>471 </word></p><p><word>She </word><word>thrust </word><word>forward </word><word>through </word><word>the </word><word>shadows </word><word>and </word><word>the </word><word>trees </word><word>that </word><dep_head>resisted_dobj_head </dep_head><dep>her_dobj_dep </dep><word>and </word><word>tried </word><word>to </word><word>fling </word><word>her </word><word>back </word><word>. </word><word>
 </word><word>226 </word></p><p><word>The </word><word>most </word><word>infamous </word><word>of </word><word>all </word><word>was </word><word>launched </word><word>by </word><word>the </word><word>explosion </word><word>of </word><word>the </word><word>island </word><word>of </word><word>Krakatoa </word><word>in </word><word>1883 </word><word>; </word><word>; </word><word>it </word><word>raced </word><word>across </word><word>the </word><word>Pacific </word><word>at </word><word>300 </word><word>miles </word><word>an </word><word>hour </word><word>, </word><dep_head>devastated_dobj_head </dep_head><word>the </word><dep>coasts_dobj_dep </dep><word>of </word><word>Java </word><word>and </word><word>Sumatra </word><word>with </word><word>waves </word><word>100 </word><word>to </word><word>130 </word><word>feet </word><word>high </word><word>, </word><word>and </word><word>pounded </word><word>the </word><word>shore </word><word>as </word><word>far </word><word>away </word><word>as </word><word>San </word><word>Francisco </word><word>. </word><word>
 </word><word>40 </word></p></html>
