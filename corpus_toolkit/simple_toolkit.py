#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 08:00:19 2019

@author: kkyle2
"""
#version .09 - common error handling include load corpus issues
#version .05-.08 minor bug fixes
#version .04 2019-8-12 adds code for reading lemma file while part of package
#version .03 2019-8-11 includes more minor bug fixes 
#version .02 2019-8-9
#includes a number of minor bug fixes
import glob
import math
import operator
import math
#for writing modified corpus files
import os
import pkg_resources

data_filename = pkg_resources.resource_filename('corpus_toolkit', 'antbnc_lemmas_ver_003.txt')


def write_corpus(dirname,new_dirname,corpus,ending = "txt"):
	dirsep = os.path.sep
	name_list = []
	for x in glob.glob(dirname + "/*" + ending):
		simple_name = x.split(dirsep)[-1] #split the long directory name by the file separator and take the last item (the short filename)
		name_list.append(simple_name)
	if len(name_list) != len(corpus):
		print("Your directory name and your corpus don't match. Please correct this and try again")
		return
	try:	
		os.mkdir(new_dirname + "/") #make the new folder
	except FileExistsError: #if folder already exists, then print message
		print("Writing files to existing folder")
		
	for i, document in enumerate(corpus): #use enumerate to iterate through the corpus list
		new_filename = new_dirname + "/" + name_list[i] #create new filename
		outf = open(new_filename,"w") #create outfile with new filename
		corpus_string = " ".join(document) #turn corpus list into string
		outf.write(corpus_string) #write corpus list
		outf.flush()
		outf.close()
	
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
#family_dict = load_lemma("classic_familizer_dict_antconc.txt")

#this function will load the whole corpus into memory. This is fine for small to medium-sized corpora, but won't work with huge corpora
def load_corpus(dir_name, ending = '.txt', lower = True): #this function takes a directory/folder name as an argument, and returns a list of strings (each string is a document)
	master_corpus = [] #empty list for storing the corpus documents
	filenames = glob.glob(dir_name + "/*" + ending) #make a list of all ".txt" files in the directory
	
	if len(filenames) == 0:
		doc_check(filenames,dir_name,ending)
		return(None)

	for filename in filenames: #iterate through the list of filenames
		if lower == True:
			master_corpus.append(open(filename, errors = "ignore").read().lower()) #open each file, lower it and add strings to list
		else:
			master_corpus.append(open(filename, errors = "ignore").read())#open each file, (but don't lower it) and add strings to list
			
	return(master_corpus) #output list of strings (i.e., the corpus)


default_punct_list = [",",".","?","'",'"',"!",":",";","(",")","[","]","''","``","--"] #we can add more items to this if needed
default_space_list = ["\n","\t","    ","   ","  "]

def tokenize(corpus_list, remove_list = default_punct_list, space_list = default_space_list, split_token = " "):
	master_corpus = [] #holder list for entire corpus
	
	for text in corpus_list: #iterate through each string in the corpus_list
		for item in remove_list:
			text = text.replace(item,"") #replace each item in list with "" (i.e., nothing)
		for item in space_list:
			text = text.replace(item," ")
			
		#then we will tokenize the document and add it to the corpus
		tokenized = text.split(split_token) #split string into list using the split token (by default this is a space " ")
	
		master_corpus.append(tokenized) #add tokenized text to the master_corpus list
	
	return(master_corpus)



def lemmatize(tokenized_corpus,lemma = lemma_dict): #takes a list of lists (a tokenized corpus) and a lemma dictionary as arguments
	master_corpus = [] #holder for lemma corpus
	for text in tokenized_corpus: #iterate through corpus documents
		lemma_text = [] #holder for lemma text
		
		for word in text: #iterate through words in text
			if word in lemma: #if word is in lemma dictionary
				lemma_text.append(lemma[word]) #add the lemma for to lemma_text
			else:
				lemma_text.append(word) #otherwise, add the raw word to the lemma_text
		
		master_corpus.append(lemma_text) #add lemma version of the text to the master corpus
	
	return(master_corpus) #return lemmatized corpus
		
#n-grams
#Takes a tokenized list and converts it into a list of n-grams
def ngrammer(tokenized_corpus,number):
	master_ngram_list = [] #list for entire corpus
	
	for tokenized in tokenized_corpus:
		ngram_list = [] #empty list for ngrams
		last_index = len(tokenized) - 1 #this will let us know what the last index number is
		for i , token in enumerate(tokenized): #enumerate allows us to get the index number for each iteration (this is i) and the item
			if i + number > last_index: #if the next index doesn't exist (because it is larger than the last index)
				continue
			else:
				ngram = tokenized[i:i+number] #the ngram will start at the current word, and continue until the nth word
				ngram_string = "_".join(ngram) #turn list of words into an n-gram string
				ngram_list.append(ngram_string) #add string to ngram_list
		
		master_ngram_list.append(ngram_list) #add ngram_list to master list
		
	return(master_ngram_list)
		 

ignore_list = [""," ", "  ", "   ", "    "] #list of items we want to ignore in our frequency calculations

def corpus_frequency(corpus_list, ignore = ignore_list, calc = 'freq', normed = False): #options for calc are 'freq' or 'range'
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


def keyness(freq_dict1,freq_dict2,effect = "log-ratio"): #this assumes that raw frequencies were used. effect options = "log-ratio", "%diff", "odds-ratio"
	keyness_dict = {}
	ref_dict = {}
	
	size1 = sum(freq_dict1.values())
	size2 = sum(freq_dict2.values())
	
	def log_ratio(freq1,size1,freq2,size2): #presumes that the frequencies are normed
		freq1_norm = freq1/size1 * 1000000
		freq2_norm = freq2/size2 * 1000000
		index = math.log2(freq1/freq2)
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
			
	
	#create combined word list (we will actually use a dictionary for speed)
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

##############################
### Write Output to a file ###
##############################

def list_writer(outf_name,dict_list,header_list = ["word","frequency"],cutoff = 5, sep = ","):
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
	

def collocator(corpus_list,target, left = 4,right = 4, stat = "MI", cutoff = 5): #returns a dictionary of collocation values
	corp_freq = corpus_frequency(corpus_list) #use the corpus_frequency function to create frequency list
	nwords = sum(corp_freq.values()) #get corpus size for statistical calculations
	collocate_freq = {} #empty dictionary for storing collocation frequencies
	r_freq = {} #for hits to the right
	l_freq = {}  #for hits to the left
	stat_dict = {} #for storing the values for whichever stat was used
	
	def freq(l,d): #this takes a list (l) and a dictionary (d) as arguments
		for x in l: #for x in list
			if x not in d: #if x not in dictionary
				d[x] = 1 #create new entry
			else: #else: add one to entry
				d[x] += 1
	
	#begin collocation frequency analysis
	for text in corpus_list:
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


def high_val(stat_dict,hits = 20,hsort = True,output = False,filename = None, sep = "\t"):
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






