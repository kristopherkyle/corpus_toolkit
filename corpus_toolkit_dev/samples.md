#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 11:27:50 2019

@author: kkyle2
"""

corp1 = tokenize(ldcorpus("brown_single")) #note that corp is a generator... so you have to redefine it after you use it.

freq = frequency(corp1)
head(freq)
head(freq,50)

tg_freq = frequency(tag(ldcorpus("brown_single")))
head(tg_freq)

write_corpus("tagged_brown_single",tag(ldcorpus("brown_single")))

write_corpus("tagged_brown_single",tag(ldcorpus("brown_single")),"brown_single")

reload_freq = frequency(reload("tagged_brown_single"))
head(reload_freq)

tg_bg_freq = frequency(tag(ldcorpus("brown_single"),ngram = 3))
head(tg_freq)

ngfreq = frequency(tokenize(ldcorpus("brown_single"),lemma = False,ngram = 3))
head(ngfreq)

collocates = collocator(tokenize(ldcorpus("brown_single")),"went")
head(collocates)

bg_dict = dep_bigram(ldcorpus("brown_single"),"dobj")
head(bg_dict["bi_freq"])

dep_conc(bg_dict["samples"],"dobj_results") # be sure to set your working directory!

brown_soa = soa(bg_dict)
head(brown_soa)
