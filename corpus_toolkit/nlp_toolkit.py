#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 06:22:09 2019

@author: kkyle2
"""
#version .09 - common error handling include load corpus issues
#version .05-.08 minor bug fixes
#version .04 2019-8-12; adds bug fixes
#version .03 2019-08-11; adds dependency bigram functions (including strenght of association and concordancing)
#version .02 2019-8-9; includes a number of minor bug fixes

import glob
import math
try:
	import spacy #import spacy
except ModuleNotFoundError:
	print("It appears that you do not have spacy installed on your computer. Without installing Spacy, this package won't work properly.")
try:	
	nlp = spacy.load("en_core_web_sm") #load the English model. This can be changed - just make sure that you download the appropriate model first
except ImportError:
	print("It appears that you haven't downloaded the default language model for Spacy 'en_core_web_sm'. Please make sure you have a model downloaded. If you wish to use a model other than the default one, then load it before proceeding: 'nlp = spacy.load('model_name')'")

def doc_check(f_list,dirname,ending):
	if len(f_list) == 0:
		print("\nNo files with the ending '" + ending + "' were found in a directory/folder entitled '" + dirname + "'.\n\n" + "Please check to make sure that:\n1. You have set your working directory\n2. Your directory/folder name is spelled correctly\n3. '" + ending +"' matches the ending of your filenames")
	else:
		print(len(f_list) + " files ending in " + ending + " found in the " + dirname + " folder.")

def tag(text,tp = "upos", lemma = True, lower = True, connect = "_",ignore = ["PUNCT","SPACE","SYM"]):
	
	#check to make sure a valid tag was chosen
	if tp not in ["penn","upos","dep"]:
		print("Please use a valid tag type: 'penn','upos', or 'dep'")
		return #exit the function
	
	else:
		doc = nlp(text) #use spacy to tokenize, lemmatize, pos tag, and parse the text
		text_list = [] #empty list for output
		for token in doc: #iterate through the tokens in the document
			if token.pos_ in ignore: #if the universal POS tag is in our ignore list, then move to next word
				continue
			
			if lemma == True: #if we chose lemma (this is the default)
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
		
		return(text_list) #return text list
		
		
def tag_corpus(dirname, ending = ".txt", tp = "upos", lemma = True, lower = True, connect = "_",ignore = ["PUNCT","SPACE"]):
	filenames = glob.glob(dirname + "/*" + ending) #gather all text names
	
	if len(filenames) == 0:
		doc_check(filenames,dirname,ending)
		return(None)
		
	master_corpus = [] #holder for total corpus
	
	file_count  = 1 #this is to give the user updates about the pogram's progress
	total = len(filenames) #this is the total number of files to process
	for filename in filenames: #iterate through corpus filenames
		#user message
		print("Tagging " + str(file_count) + " of " + str(total) + " files.")
		file_count += 1 #add one to the file_count
		
		raw_text = open(filename, errors = "ignore").read() #open each file
		master_corpus.append(tag(raw_text,tp,lemma,lower,connect,ignore)) #add the tagged text to the master list
	
	return(master_corpus) #return list
	
def dep_bg_simple(text,dep): #for teaching purposes
	dep_list = [] #list for dependency bigrams
	doc = nlp(text) #tokenize, tag, and parse text
	
	for token in doc: #iterate through tokens
		
		if token.dep_ == dep: #if the dependency relationship matches 
			dependent = token.lemma_ #extract the lemma of the dependent
			head = token.head.lemma_ #extract the lemma of the head
			
			dep_bigram = dependent + "_" + head #create a dep_head string

			dep_list.append(dep_bigram) #add dep_head string to list
	
	return(dep_list)
	
def dep_bigram_corpus(dirname,dep,ending = ".txt", lemma = True, lower = True, dep_upos = None, head_upos = None, dep_text = None, head_text = None):
	filenames = glob.glob(dirname + "/*" + ending) #gather all text names
	
	if len(filenames) == 0:
		doc_check(filenames,dirname,ending)
		return(None)

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

	file_count  = 1 #this is to give the user updates about the pogram's progress
	total = len(filenames) #this is the total number of files to process
	
	for filename in filenames: #iterate through corpus filenames
		#user message
		print("Tagging " + str(file_count) + " of " + str(total) + " files.")
		file_count += 1 #add one to the file_count
		
		text = open(filename, errors = "ignore").read() #open each file
		doc = nlp(text) #tokenize, tag, and parse text using spaCy
		range_list = [] #for range information
		#sent_text = "first"
		for sentence in doc.sents: #iterate through sentences
			#print(sent_text)
			index_start = 0 #for identifying sentence-level indexes later
			sent_text = [] #holder for sentence
			dep_headi = [] #list for storing [dep,head] indexes
			first_token = True #for identifying index of first token
			
			for token in sentence: #iterate through parsed spaCy document
				if first_token == True:
					index_start = token.i #if this is the first token, set the index start number
					first_token = False #then set first token to False
				
				sent_text.append(token.text) #for adding word to sentence
				
				if token.dep_ == dep: #if the token's dependency tag matches the one designated
					dep_tg = token.pos_ #get upos tag for the dependent (only used if dep_upos is specified)
					head_tg = token.head.pos_ #get upos tag for the head (only used if dep_upos is specified)
					
					if lemma == True: #if lemma is true, use lemma form of dependent and head
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
				
				temp_sent.append(filename) ## add filename to sent to indicate where example originated
				match_sentences.append(temp_sent) #add temporary sentence to match_sentences for output
		
		for x in list(set(range_list)): #create a type list of the dep_bigrams in the text
			dicter(x,range_freq) #add document counts to the range_freq dictionary
			

	bigram_dict = {"bi_freq":bi_freq,"dep_freq":dep_freq,"head_freq": head_freq, "range":range_freq, "samples":match_sentences} #create a dictioary of dictionaries
	return(bigram_dict) # return dictionary of dictionaries

def bigram_soa(freq_dict,stat = "MI", range_cutoff = 5, cutoff=5):
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

import xml.etree.ElementTree as ET #for writing xml or html
import random


def dep_conc(example_list,hits = 50, filename = "results",seed = None):
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
		
