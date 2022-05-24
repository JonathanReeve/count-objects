#!/usr/bin/env python
# coding: utf-8
from nltk.corpus import wordnet as wn
import re
from collections import Counter
import pandas as pd
from plotly import express as px
import argparse
import json

def parseResults(fn): 
    with open(fn) as f: 
        results = f.read()
    pat = r"\(([0-9]+), ([0-9]+), (.*?), Synset\('(.*?)'\)"
    matches = re.findall(pat, results)
    parsed = []
    for match in matches: 
        parI, wordI, word, syn = match
        parsed.append((int(parI), int(wordI), word, wn.synset(syn)))
    return parsed

def categorizeWords(data, minDepth=5, maxDepth=0):
    wordsAndCats = []
    for word, val in data.items():
        wordCat = [val, word]
        depth = minDepth
        while depth > maxDepth:
            cat = getHypernymLevelN(word, depth).name()
            wordCat.append(cat)
            depth -= 1
        wordsAndCats.append(wordCat)
    return wordsAndCats

def getHypernymLevelN(synset, n):
    while synset.min_depth() > n:
        hypernyms = synset.hypernyms()
        if len(hypernyms) > 0:
            synset = hypernyms[0]
        else:
            break
    return synset

def makeChart(colorWithCats, name):
    df = pd.DataFrame(colorWithCats) # columns=cols)
    #print(df)
    fig = px.treemap(df, path=df.columns[-1:0:-1],
                     values=0,
                     color=0,
                     #color_continuous_scale=getColorScale(name),
                     color_continuous_midpoint=df[0].mean(),
                     title='Breakdown of objects in ' + name
                     )
    with open(name+'.html', 'w') as f:
        f.write(fig.to_html())
    return df 


def percentInCat(categorized, query): 
    """ Calculate the percentage of a given category. 
    The objects in this texts are X% objects, for instance." 
    """
    return len([l for l in categorized if query in l[2:]]) / len(categorized)


def objectPercentages(categorized, cats=['artifact.n.01', 'living_thing.n.01', 'natural_object.n.01']): 
    out = {}
    for cat in cats: 
        percent = percentInCat(categorized, cat)
        out[cat] = percent
    return out

def artifacts(categorized):
    objects = {}
    for item in categorized:
        # Skip the first two, which aren't iterable
        sublist = item[2:]
        if 'artifact.n.01' in sublist:
            artifactIdx = sublist.index('artifact.n.01')
            if artifactIdx > 0:
                artifactHypo = sublist[artifactIdx-1]  # Get the previous item
                if artifactHypo in objects:
                    objects[artifactHypo] += item[0]  # Sum all the counts
                else:
                    objects[artifactHypo] = item[0]
    return objects

def macroStats(fn):
    return {fn: objectPercentages(categorized)}

def artifactHyponyms(fn):
    return {fn: artifacts(categorized)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count the number of objects in a text, according to their WordNet categories.")
    parser.add_argument('filename')
    parser.add_argument('--verbose', action='store_true', help="Print out everything")
    parser.add_argument('--artifacts', action='store_true', help="Print out statistics about artifacts")
    args = parser.parse_args()
    fn = args.filename
    results = parseResults(fn)
    stats = Counter([item[3] for item in results])
    categorized = categorizeWords(stats)
    # results = macroStats(fn)
    results = artifactHyponyms(fn)
    print(json.dumps(results))
