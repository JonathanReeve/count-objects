#!/usr/bin/env python
# coding: utf-8
from nltk.corpus import wordnet as wn
import re
from collections import Counter
import pandas as pd
from plotly import express as px
import argparse
import json
from glob import glob

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


def percentInCat(categorized, query, fn, wordCount):
    """ Calculate the percentage of a given category.
    The objects in this texts are X% objects, for instance."
    """
    return len([l for l in categorized if query in l[2:]]) / wordCount


def objectPercentages(categorized, fn, counts):
    out = {}
    cats = ['artifact.n.01', 'living_thing.n.01', 'natural_object.n.01']
    for cat in cats: 
        percent = percentInCat(categorized, cat, fn, counts)
        out[cat] = percent
    return out


def artifacts(categorized, fn, count):
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
    # Divide by word counts
    objectFrequencies = {}
    for sense, n in objects.items():
        objectFrequencies[sense] = (n / count) * 100
    return objectFrequencies


def main():
    counts = json.load(open("wordCounts.json"))

    allObjects = {}
    allArtifacts = {}

    allResults = glob('results/*')

    for i, fn in enumerate(allResults):
        print(f"Processing {fn}, {i} of {len(allResults)}")
        basename = fn.split("/")[-1].strip(".json")
        wordCount = counts[basename]
        results = parseResults(fn)
        stats = Counter([item[3] for item in results])
        categorized = categorizeWords(stats)
        # makeChart(categorized, fn)
        allObjects[fn] = objectPercentages(categorized, fn, wordCount)
        allArtifacts[fn] = artifacts(categorized, fn, wordCount)

    with open("objects.json", 'w') as f:
        json.dump(allObjects, f, indent=2)

    with open("artifacts.json", 'w') as f:
        json.dump(allArtifacts, f, indent=2)


if __name__ == "__main__":
    main()
