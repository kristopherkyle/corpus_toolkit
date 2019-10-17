#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 10:49:52 2019

@author: kkyle2
"""

import glob
import math
import pkg_resources
import operator
import itertools
import xml.etree.ElementTree as ET #for writing xml or html
import random
import os

version = "0.20"

try:
	import spacy #import spacy
except ModuleNotFoundError:
	print("It appears that you do not have spacy installed on your computer. Without installing Spacy, the tag(), and tag_corpus() functions won't work properly.")
try:	
	nlp = spacy.load("en_core_web_sm") #load the English model. This can be changed - just make sure that you download the appropriate model first
except ImportError:
	print("It appears that you haven't downloaded the default language model for Spacy 'en_core_web_sm'. Please make sure you have a model downloaded. If you wish to use a model other than the default one, then load it before proceeding: 'nlp = spacy.load('model_name')'")

data_filename = pkg_resources.resource_filename('corpus_toolkit', 'antbnc_lemmas_ver_003.txt')

dirsep = os.path.sep
default_punct_list = [",",".","?","'",'"',"!",":",";","(",")","[","]","''","``","--"] #we can add more items to this if needed
default_space_list = ["\n","\t","    ","   ","  "]

def doc_check(f_list,dirname,ending):
	if len(f_list) == 0:
		print("\nNo files with the ending '" + ending + "' were found in a directory/folder entitled '" + dirname + "'.\n\n" + "Please check to make sure that:\n1. You have set your working directory\n2. Your directory/folder name is spelled correctly\n3. '" + ending +"' matches the ending of your filenames")
	else:
		print(len(f_list) + " files ending in " + ending + " found in the " + dirname + " folder.")

def load_lemma(lemma_file): #this is how we load a lemma_list
	lemma_dict = {} #empty dictionary for {token : lemma} key : value pairs
	lemma_list = open(lemma_file, errors = "ignore").read() #open lemma_list
	lemma_list = lemma_list.replace("\t->","") #replace marker, if it exists
	lemma_list = lemma_list.split("\n") #split on newline characters
	for line in lemma_list: #iterate through each line
		tokens = line.split("\t") #split each line into tokens
		if len(tokens) <= 2: #if there are only two items in the token list, skip the item (this fixed some problems with the antconc list)
			continue
		lemma = tokens[0] #the lemma is the first item on the list
		for token in tokens[1:]: #iterate through every token, starting with the second one
			if token in lemma_dict:#if the token has already been assigned a lemma - this solved some problems in the antconc list
				continue
			else: 
				lemma_dict[token] = lemma #make the key the word, and the lemma the value
	
	return(lemma_dict)

lemma_dict = load_lemma(data_filename)

def lemmatize(text,lemma = lemma_dict): #takes a list words (a tokenixed document) and a lemma dictionary as arguments
	lemma_text = [] #holder for lemma text
	for word in text: #iterate through words in text
		if word in lemma: #if word is in lemma dictionary
			lemma_text.append(lemma[word]) #add the lemma for to lemma_text
		else:
			lemma_text.append(word) #otherwise, add the raw word to the lemma_text
	return(lemma_text) #return lemmatized text

def ngrammer(tokenized,number,connect = "__"):
	ngram_list = [] #empty list for ngrams
	last_index = len(tokenized) - 1 #this will let us know what the last index number is
	for i , token in enumerate(tokenized): #enumerate allows us to get the index number for each iteration (this is i) and the item
		if i + number > last_index: #if the next index doesn't exist (because it is larger than the last index)
			continue
		else:
			ngram = tokenized[i:i+number] #the ngram will start at the current word, and continue until the nth word
			ngram_string = connect.join(ngram) #turn list of words into an n-gram string
			ngram_list.append(ngram_string) #add string to ngram_list
	
	return(ngram_list) #add ngram_list to master list

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

def reload(dirname,ending = ".txt",verbose = True, split_token = " "): #for reloading processed texts from file
		filenames = glob.glob(dirname + "/*" + ending) #gather all text names
		nfiles = len(filenames) #get total number of files in corpus
		fcount = 0 #counter for corpus files
		for x in filenames:
			fcount +=1 #update file count
			sm_fname = x.split(dirsep)[-1] # get filename
			if verbose == True:
				print("Processing", sm_fname, "(" + str(fcount), "of", nfiles,"files)")
			text = open(x, errors = "ignore").read()
			tokenized = text.split(split_token) #split string into list using the split token (by default this is a space " ")
			yield(tokenized)


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

def tag(corpus,tp = "upos", lemma = True, pron = False, lower = True, connect = "_",ignore = ["PUNCT","SPACE","SYM"],ngram = False,ngrm_connect = "__"):
	
	#check to make sure a valid tag was chosen
	if tp not in ["penn","upos","dep"]:
		print("Please use a valid tag type: 'penn','upos', or 'dep'")	
	else:
		for text in corpus:
			doc = nlp(text) #use spacy to tokenize, lemmatize, pos tag, and parse the text
			text_list = [] #empty list for output
			for token in doc: #iterate through the tokens in the document
				if token.pos_ in ignore: #if the universal POS tag is in our ignore list, then move to next word
					continue
				
				if lemma == True: #if we chose lemma (this is the default)
					if pron == False: #if we don't want Spacy's pronoun lemmatization
						if token.lemma_ == "-PRON-":
							word = token.text.lower() #then use the raw form of the word
						else:
							word = token.lemma_ #otherwise the word form will be a lemma
					else:
						word = token.lemma_ #then the word form will be a lemma
				else:
					if lower == True: #if we we chose lemma = False but we want our words lowered (this is default)
						word = token.text.lower() #then lower the word
					else:
						word = token.text #if we chose lemma = False and lower = False, just give us the word
				
				if tp == None: #if tp = None, then just give the tokenized word (and nothing else)
					text_list.append(word)
				
				else:
					if tp == "penn":
						tagged = token.tag_ #modified penn tag
					elif tp == "upos":
						tagged = token.pos_ #universal pos tag
					elif tp == "dep":
						tagged = token.dep_ #dependency relationship
				
				tagged_token = word + connect + tagged #add word, connector ("_" by default), and tag
				text_list.append(tagged_token) #add to list
			
			if ngram != False:
				text_list = ngrammer(text_list,ngram,ngrm_connect)
			yield(text_list) #yield text list

def write_corpus(new_dirname,corpus, dirname = False, ending = "txt"):
	name_list = []
	if dirname != False:
		for x in glob.glob(dirname + "/*" + ending):
			simple_name = x.split(dirsep)[-1] #split the long directory name by the file separator and take the last item (the short filename)
			name_list.append(simple_name)

	try:	
		os.mkdir(new_dirname + "/") #make the new folder
	except FileExistsError: #if folder already exists, then print message
		print("Writing files to existing folder")
		
	for i, document in enumerate(corpus): #use enumerate to iterate through the corpus list
		if dirname == False:
			new_filename = new_dirname + "/" + str(i+1) + "." + ending #create new filename
		else:
			new_filename = new_dirname + "/" + name_list[i] #create new filename
		outf = open(new_filename,"w") #create outfile with new filename
		corpus_string = " ".join(document) #turn corpus list into string
		outf.write(corpus_string) #write corpus list
		outf.flush()
		outf.close()

ignore_list = [""," ", "  ", "   ", "    "] #list of items we want to ignore in our frequency calculations

def frequency(corpus_list, ignore = ignore_list, calc = 'freq', normed = False): #options for calc are 'freq' or 'range'
	freq_dict = {} #empty dictionary
	
	for tokenized in corpus_list: #iterate through the tokenized texts
		if calc == 'range': #if range was selected:
			tokenized = list(set(tokenized)) #this creates a list of types (unique words)
		
		for token in tokenized: #iterate through each word in the texts
			if token in ignore_list: #if token is in ignore list
				continue #move on to next word
			if token not in freq_dict: #if the token isn't already in the dictionary:
				freq_dict[token] = 1 #set the token as the key and the value as 1
			else: #if it is in the dictionary
				freq_dict[token] += 1 #add one to the count
	
	### Normalization:
	if normed == True and calc == 'freq':
		corp_size = sum(freq_dict.values()) #this sums all of the values in the dictionary
		for x in freq_dict:
			freq_dict[x] = freq_dict[x]/corp_size * 1000000 #norm per million words
	elif normed == True and calc == "range":
		corp_size = len(corpus_list) #number of documents in corpus
		for x in freq_dict:
			freq_dict[x] = freq_dict[x]/corp_size * 100 #create percentage (norm by 100)
	
	return(freq_dict)

def head(stat_dict,hits = 20,hsort = True,output = False,filename = None, sep = "\t"):
	#first, create sorted list. Presumes that operator has been imported
	sorted_list = sorted(stat_dict.items(),key=operator.itemgetter(1),reverse = hsort)[:hits]
	
	if output == False and filename == None: #if we aren't writing a file or returning a list
		for x in sorted_list: #iterate through the output
			print(x[0] + "\t" + str(x[1])) #print the sorted list in a nice format
	
	elif filename is not None: #if a filename was provided
		outf = open(filename,"w") #create a blank file in the working directory using the filename
		for x in sorted_list: #iterate through list
			outf.write(x[0] + sep + str(x[1])+"\n") #write each line to a file using the separator
		outf.flush() #flush the file buffer
		outf.close() #close the file

	if output == True: #if output is true
		return(sorted_list) #return the sorted list

def list_writer(outf_name,dict_list,header_list = ["item","stat"],cutoff = 5, sep = ","):
	outf = open(outf_name, "w") #create output file
	
	outf.write(",".join(header_list) + "\n") #turn header_list into a string, then write the header
	
	#use the first dictionary in the dict_list for the basis of sorting
	#this will output a list of (word,frequency) tuples
	sorted_list = sorted(dict_list[0].items(),key=operator.itemgetter(1),reverse = True)
	
	for x in sorted_list: #iterate through (word, frequency) list items
		word = x[0]
		freq = x[1]
		if freq < cutoff: #if the frequency doesn't meet the frequency cutoff
			continue #skip that item
		out_list = [word] #create list for output that includes the word
		for entry in dict_list: #iterate through all dictionaries in the dict_list (there may only be one)
			if word in entry: #make sure entry is in dictionary
				out_list.append(str(entry[word])) #add the value to the list. Note, we convert the value to a string using str()
			else:
				out_list.append("0") #if it isn't in the dictioanary, set it to "0"
		
		outf.write(sep.join(out_list) + "\n") #write the line to the file
	
	outf.flush() #flush the buffer
	outf.close()#close the file
	print("Finished writing file")

def keyness(freq_dict1,freq_dict2,effect = "log-ratio"): #this assumes that raw frequencies were used. effect options = "log-ratio", "%diff", "odds-ratio"
	keyness_dict = {}
	ref_dict = {}
	
	size1 = sum(freq_dict1.values())
	size2 = sum(freq_dict2.values())
	
	def log_ratio(freq1,size1,freq2,size2): 
		freq1_norm = freq1/size1 * 1000000
		freq2_norm = freq2/size2 * 1000000
		index = math.log2(freq1_norm/freq2_norm)
		return(index)
	
	def perc_diff(freq1,size1,freq2,size2):
		freq1_norm = freq1/size1 * 1000000
		freq2_norm = freq2/size2 * 1000000
		index = ((freq1_norm-freq2_norm)  * 100)/freq2_norm
		return(index)
	
	def odds_ratio(freq1,size1,freq2,size2):
		if size1 - freq1 == 0: #this will be a very rare case, but would kill program
			size1 += 1
		if size2 - freq2 == 0: #this will be a very rare case, but would kill program
			size2 += 1
		index = (freq1/(size1-freq1))/(freq2/(size2-freq2))
		return(index)
			
	
	#create combined word list (we actually use a dictionary for speed)
	for x in freq_dict1:
		if x not in ref_dict:
			ref_dict[x] = 0 #the zero isn't used for anything
	for x in freq_dict2:
		if x not in ref_dict:
			ref_dict[x] = 0 #the zero isn't used for anything
	
	#if our item doesn't occur in one of our reference corpora, we need to make an adjustment
	#here, we change the frequency to a very small number (.00000001) instead of zero
	#this is because zeros will cause problems in our calculation of keyness
	for item in ref_dict:
		if item not in freq_dict1 or freq_dict1[item] == 0:
			freq_dict1[item] = .00000001 #tiny number
		if item not in freq_dict2 or freq_dict2[item] == 0:
			freq_dict2[item] = .00000001 #tiny number
		
		if effect == 'log-ratio':
			keyness_dict[item] = log_ratio(freq_dict1[item],size1,freq_dict2[item],size2)
		
		elif effect == "%diff":
			keyness_dict[item] = perc_diff(freq_dict1[item],size1,freq_dict2[item],size2)
		
		elif effect == "odds-ratio":
			keyness_dict[item] = odds_ratio(freq_dict1[item],size1,freq_dict2[item],size2)

	return(keyness_dict)

def collocator(corpus,target, left = 4,right = 4, stat = "MI", cutoff = 5, ignore=ignore_list): #returns a dictionary of collocation values
	
	corpus, freq_corp = itertools.tee(corpus) #this makes two versions of the iterator so that it can be processed twice
	corp_freq = corpus_frequency(freq_corp) #use the corpus_frequency function to create frequency list
	nwords = sum(corp_freq.values()) #get corpus size for statistical calculations
	collocate_freq = {} #empty dictionary for storing collocation frequencies
	r_freq = {} #for hits to the right
	l_freq = {}  #for hits to the left
	stat_dict = {} #for storing the values for whichever stat was used
	
	def freq(l,d): #this takes a list (l) and a dictionary (d) as arguments
		for x in l: #for x in list
			if x in ignore:
				continue
			if x not in d: #if x not in dictionary
				d[x] = 1 #create new entry
			else: #else: add one to entry
				d[x] += 1
	
	#begin collocation frequency analysis
	for text in corpus:
		if target not in text: #if target not in the text, don't search it for other words
			continue
		else:
			last_index = len(text) -1 #get last index number
			for i , word in enumerate(text):
				if word == target:
					start = i-left #beginning of left span
					end = i + right + 1 #end of right span. Note, we have to add 1 because of the way that slices work in python
					if start < 0: #if the left span goes beyond the text
						start = 0 #start at the first word
					#words to the right
					lspan_list = text[start:i] #for counting words on right
					freq(lspan_list,l_freq) #update l_freq dictionary
					freq(lspan_list,collocate_freq) #update collocate_freq dictionary
					
					rspan_list = text[i+1:end] #for counting words on left. Note, have to add +1 to ignore node word
					freq(rspan_list,r_freq) #update r_freq dictionary
					freq(rspan_list,collocate_freq) #update collocate_freq dictionary
	
	#begin collocation stat calculation

	for x in collocate_freq:
		observed = collocate_freq[x]
		if observed < cutoff: #if the collocate frequency doesn't meet the cutoff, ignore it
			continue
		else:
			expected = (corp_freq[target] * corp_freq[x])/nwords #expected = (frequency of target word (in entire corpus) * frequency of collocate (in entire corpus)) / number of words in corpus
			if stat == "MI": #pointwise mutual information
				mi_score = math.log2(observed/expected) #log base 2 of observed co-occurence/expected co-occurence
				stat_dict[x] = mi_score
			elif stat == "T": #t-score
				t_score = math.log2((observed - expected)/math.sqrt(expected))
				stat_dict[x] = t_score
			elif stat == "freq":
				stat_dict[x] = collocate_freq[x]
			elif stat == "right": #right frequency
				stat_dict[x] = r_freq[x] 
			elif stat == "left":
				stat_dict[x] = l_freq[x]
				
	return(stat_dict) #return stat dict

def dep_bigram(corpus,dep,lemma = True, lower = True, pron = False, dep_upos = None, head_upos = None, dep_text = None, head_text = None):
	
	bi_freq = {} #holder for dependency bigram frequency
	dep_freq = {} #holder for depenent frequency
	head_freq = {} #holder for head frequency
	range_freq = {}
	match_sentences = [] #holder for sentences that include matches

	def dicter(item,d): #d is a dictinoary
		if item not in d: 
			d[item] = 1
		else:
			d[item] +=1
	
	textid = 0
	for text in corpus: #iterate through corpus filenames
		textid+=1
		range_list = [] #for range information
		#sent_text = "first"
		doc = nlp(text) #tokenize, tag, and parse text using spaCy
		for sentence in doc.sents: #iterate through sentences
			#print(sent_text)
			index_start = 0 #for identifying sentence-level indexes later
			sent_text = [] #holder for sentence
			dep_headi = [] #list for storing [dep,head] indexes
			first_token = True #for identifying index of first token
			
			for token in sentence: #iterate through tokens in document
				if first_token == True:
					index_start = token.i #if this is the first token, set the index start number
					first_token = False #then set first token to False
				
				sent_text.append(token.text) #for adding word to sentence
				
				if token.dep_ == dep: #if the token's dependency tag matches the one designated
					dep_tg = token.pos_ #get upos tag for the dependent (only used if dep_upos is specified)
					head_tg = token.head.pos_ #get upos tag for the head (only used if dep_upos is specified)
					
					if lemma == True: #if lemma is true, use lemma form of dependent and head
						if pron == False: #if we don't want Spacy's pronoun lemmatization
							if token.lemma_ == "-PRON-":
								dependent = token.text.lower() #then use the raw form of the word
								headt = token.head.text.lower()
							else:
								dependent = token.lemma_
								headt = token.head.lemma_
						else:
							dependent = token.lemma_
							headt = token.head.lemma_
					
					if lemma == False: #if lemma is false, use the token form
						if lower == True: #if lower is true, lower it
							dependent = token.text.lower()
							headt = token.head.text.lower()
						else: #if lower is false, don't lower
							dependent = token.text
							headt = token.head.text
	
					if dep_upos != None and dep_upos != dep_tg: #if dependent tag is specified and upos doesn't match, skip item
						continue
					
					if head_upos != None and head_upos!= head_tg: #if head tag is specified and upos doesn't match, skip item
						continue
	
					if dep_text != None and dep_text != dependent: #if dependent text is specified and text doesn't match, skip item
						continue
					
					if head_text != None and head_text != headt: #if head text is specified and text doesn't match, skip item
						continue
	
					dep_headi.append([token.i-index_start,token.head.i-index_start]) #add sentence-level index numbers for dependent and head

					dep_bigram = dependent + "_" + headt #create dependency bigram
		
					range_list.append(dep_bigram) #add to document-level range list
					dicter(dep_bigram,bi_freq) #add values to frequency dictionary
					dicter(dependent,dep_freq) #add values to frequency dictionary
					dicter(headt,head_freq) #add values to frequency dictionary
		
			### this section is for creating a list of sentences that include our hits ###
			for x in dep_headi: #iterate through hits
				
				temp_sent = sent_text.copy() #because there may be multiple hits in each sentence (but we only want to display one hit at at time), we make a temporary copy of the sentence that we will modify
				
				depi = sent_text[x[0]] + "_" + dep+ "_dep" #e.g., word_dobj_dep
				headi = sent_text[x[1]] + "_" + dep+ "_head" #e.g., word_dobj_head
				
				temp_sent[x[0]] = depi #change dependent word to depi in temporary sentence
				temp_sent[x[1]] = headi ##change head word to headi in temporary sentence
				
				temp_sent.append(str(textid)) ## add file inded to sent to indicate where example originated
				match_sentences.append(temp_sent) #add temporary sentence to match_sentences for output
		
		for x in list(set(range_list)): #create a type list of the dep_bigrams in the text
			dicter(x,range_freq) #add document counts to the range_freq dictionary
			

	bigram_dict = {"bi_freq":bi_freq,"dep_freq":dep_freq,"head_freq": head_freq, "range":range_freq, "samples":match_sentences} #create a dictioary of dictionaries
	return(bigram_dict) # return dictionary of dictionaries

def dep_conc(example_list,filename = "results",hits = 50, seed = None):
	random.seed(seed) #set seed
	if len(example_list) <= hits: #if the desired number of hits is more than the size of the hit list
		sample_list = example_list #just use the hit list
	else:
		sample_list = random.sample(example_list,hits) #otherwise, produce a random sample
	
	### This section builds the header material for the .html file.
	outstring = "<!doctype html>\n" ##declare formatting
	root = ET.Element("html") #create root tag
	head = ET.SubElement(root,"head") #create header
	style = ET.SubElement(head,"style") #add style tag
	style.text = "dep {color:red;} \n dep_head {color:blue;}" #set styles for dep and dep_head tags
	
	#iterate through sentences
	for sentence in sample_list:
		paragraph = ET.SubElement(root,"p") #create new paragraph 
		for token in sentence: #iterate through tokens
			if "_dep" in token: #if it is a dependent
				dep = ET.SubElement(paragraph,"dep") #use the dep tag, making it red
				dep.text = token + " " #add the text
			elif "_head" in token: #if it is a head
				dep_head = ET.SubElement(paragraph,"dep_head") #use the dep_head tag, making it blue
				dep_head.text = token + " " #add the text
			else:
				word = ET.SubElement(paragraph,"word") #otherwise, use the word tag (no special formatting)
				word.text = token + " " #add the text
	
	out_name = filename + ".html" #create filename
	outstring = outstring + ET.tostring(root,method = "html").decode("utf-8") #create output string in correct encoding
	outf = open(out_name, "w") #create file
	outf.write(outstring) #write file
	outf.flush()
	outf.close()

def soa(freq_dict,stat = "MI", range_cutoff = 5, cutoff=5):
	stat_dict = {}
	n_bigrams = sum(freq_dict["bi_freq"].values()) #get number of head_dependent in corpus for statistical calculations
	
	for x in freq_dict["bi_freq"]:
		observed = freq_dict["bi_freq"][x] #frequency of dependency bigram
		if observed < cutoff:
			continue
		if freq_dict["range"][x] > range_cutoff: #if range value doesn't meet range_cutoff, continue
			continue
		
		dep = x.split("_")[0] #split bigram into dependent and head, get dependent
		dep_freq = freq_dict["dep_freq"][dep] #get dependent frequency from dictionary
		
		head = x.split("_")[1] #split bigram into dependent and head, get head
		head_freq = freq_dict["head_freq"][head] #get head frequency from dictionary
	
		expected = ((dep_freq * head_freq)/n_bigrams) #expected = (frequency of dependent (as dependent of relationship in entire corpus) * frequency of head (of head of relationship in entire corpus)) / number of relationships in corpus
		
		#for calculating directional strength of association measures see Ellis & Gries (2015)
		a = observed
		b = head_freq - observed
		c = dep_freq - observed
		d = n_bigrams - (a+b+c)

		if stat == "MI": #pointwise mutual information
			mi_score = math.log2(observed/expected) #log base 2 of observed co-occurence/expected co-occurence
			stat_dict[x] = mi_score #add value to dictionary
		
		elif stat == "T": #t-score
			t_score = math.log2((observed - expected)/math.sqrt(expected))
			stat_dict[x] = t_score

		elif stat == "faith_dep": #probability of getting the head given the governor (e.g., getting "apple" given "red")
			faith_dep_cue = (a/(a+c))
			stat_dict[x] = faith_dep_cue
		
		elif stat == "faith_head": #probability of getting the head given the governor (e.g., getting "red" given "apple")
			faith_gov_cue = (a/(a+b))
			stat_dict[x] = faith_gov_cue

		elif stat == "dp_dep": #adjusted probability of getting the head given the governor (e.g., getting "apple" given "red")
			delta_p_dep_cue = (a/(a+c)) - (b/(b+d))
			stat_dict[x] = delta_p_dep_cue
		
		elif stat == "dp_head": #adjusted probability of getting the head given the governor (e.g., getting "red" given "apple")
			delta_p_gov_cue = (a/(a+b)) - (c/(c+d))
			stat_dict[x] = delta_p_gov_cue
	
	return(stat_dict)


