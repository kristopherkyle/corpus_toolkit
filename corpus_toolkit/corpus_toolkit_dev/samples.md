#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 11:27:50 2019

@author: kkyle2
"""

corp1 = tokenize(ldcorpus("brown_single")) #note that corp is a generator... so you have to redefine it after you use it.

freq = frequency(corp1)
head(freq,10)

head(freq,50)

tg_freq = frequency(tag(ldcorpus("brown_single")))
head(tg_freq,hits = 10)

write_corpus("tagged_brown_single",tag(ldcorpus("brown_single")))

write_corpus("tagged_brown_single",tag(ldcorpus("brown_single")),"brown_single")

reload_freq = frequency(reload("tagged_brown_single"))
head(reload_freq)

tg_bg_freq = frequency(tag(ldcorpus("brown_single"),ngram = 3))
head(tg_freq)

trigramfreq = frequency(tokenize(ldcorpus("brown_single"),lemma = False,ngram = 3))
head(trigramfreq, hits = 10)

collocates = collocator(tokenize(ldcorpus("brown_single")),"go",stat = "MI")
head(collocates)

bg_dict = dep_bigram(ldcorpus("brown_single"),"dobj")
head(bg_dict["bi_freq"], hits = 10)

dep_conc(bg_dict["samples"],"dobj_results", hits = 10) # be sure to set your working directory!

soa_mi = soa(bg_dict,stat = "MI")
head(soa_mi, hits = 10)
