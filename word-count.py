#!/usr/bin/env python3

"""
We have to get word counts from all these texts, using Spacy, since that's what we're using
in the WSD, and in order to get object counts, we need object percentages.
"""
import spacy
import argparse
import glob
import json

nlp = spacy.load('en_core_web_lg', exclude=['ner', 'tagger', 'parser', 'lemmatizer', 'tok2vec'])

nlp.max_length = 10000000

texts = glob.glob("/home/jon/Dokumentujo/Research/Corpora/pg-text/*")

wordCounts = {}

for i, text in enumerate(texts):
    with open(text) as f:
        raw = f.read()
    print(f"reading {text}, {i} of {len(texts)}")
    doc = nlp(raw)
    basename = text.split('/')[-1]
    wordCounts[basename] = int(len(doc))

with open('wordCounts.json', 'w') as f:
    json.dump(wordCounts, f)
