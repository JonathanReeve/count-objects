from nltk.corpus import wordnet as wn
from collections import Counter
import argparse
import logging
import json
from ewiser.spacy.disambiguate import Disambiguator
import spacy
import glob
import os

logging.basicConfig(level=logging.INFO)


def wsdWarmup():
    wsd = Disambiguator('ewiser/bin/ewiser.semcor+wngt.pt', lang='en',
                batch_size=5, save_wsd_details=False).eval()
    wsd = wsd.to('cuda')
    nlp = spacy.load('en_core_web_trf', disable=['ner', 'parser'])
    wsd.enable(nlp, 'wsd')
    return nlp


def wsd(paras, nlp):
    doc = nlp.pipe(paras, batch_size=5)
    return doc


def toParas(text):
    return [p for p in text.split('\n\n') if len(p) > 0]


def annotate(disambiguated):
    logging.info(f'Annotating...')
    out = ""
    for i, para in enumerate(disambiguated):
        for word in para:
            if word._.offset:
                synset = word._.synset.name()
                out += f"{word.text}//{synset} {word.whitespace_}"
            else:
                out += word.text_with_ws
    return out

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count the number of artifacts in a directory of text files, according to their WordNet categories.")
    parser.add_argument('directory')
    parser.add_argument('--verbose', action='store_true', help="Print out everything")
    args = parser.parse_args()
    directory = args.directory
    allFiles = sorted(glob.glob(directory + "/*"))

    logging.info(f"Analyzing files {allFiles}")

    logging.info("Warming up WSD...")
    nlp = wsdWarmup()


    for thisFile in allFiles:
        logging.info(f"Now analyzing file {thisFile}")
        basename = thisFile.split("/")[-1]
        outfile = f"results-pg2/{basename}-annotated.txt"
        if os.path.isfile(outfile):
            logging.info(f"Skipping {thisFile}, since we already have it.")
            continue

        try:
            with open(thisFile) as f:
                raw = f.read()
        except:
            try:
                with open(thisFile, encoding='latin1') as f:
                    raw = f.read()
            except:
                logging.info(f"Problem with {thisFile}, skipping.") 
                continue

        paras = toParas(raw)
        nParas = len(paras)

        logging.info(f'Disambiguating {nParas} paragraphs...')
        disambiguated = wsd(paras, nlp)

        annotated = annotate(disambiguated)

        with open(outfile, 'w') as f:
            f.write(annotated)
from collections import Counter
import argparse
import logging
import json
from ewiser.spacy.disambiguate import Disambiguator
import spacy
import glob
import os

logging.basicConfig(level=logging.INFO)


def wsdWarmup():
    wsd = Disambiguator('ewiser/bin/ewiser.semcor+wngt.pt', lang='en',
                batch_size=5, save_wsd_details=False).eval()
    wsd = wsd.to('cuda')
    nlp = spacy.load('en_core_web_trf', disable=['ner', 'parser'])
    wsd.enable(nlp, 'wsd')
    return nlp


def wsd(paras, nlp):
    doc = nlp.pipe(paras, batch_size=5)
    return doc


def toParas(text):
    return [p for p in text.split('\n\n') if len(p) > 0]


def annotate(disambiguated):
    logging.info(f'Annotating...')
    out = ""
    for i, para in enumerate(disambiguated):
        for word in para:
            if word._.offset:
                synset = word._.synset.name()
                out += f"{word.text}//{synset} {word.whitespace_}"
            else:
                out += word.text_with_ws
    return out

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count the number of artifacts in a directory of text files, according to their WordNet categories.")
    parser.add_argument('directory')
    parser.add_argument('--verbose', action='store_true', help="Print out everything")
    args = parser.parse_args()
    directory = args.directory
    allFiles = sorted(glob.glob(directory + "/*"))

    logging.info(f"Analyzing files {allFiles}")

    logging.info("Warming up WSD...")
    nlp = wsdWarmup()


    for thisFile in allFiles:
        logging.info(f"Now analyzing file {thisFile}")
        basename = thisFile.split("/")[-1]
        outfile = f"results-pg2/{basename}-annotated.txt"
        if os.path.isfile(outfile):
            logging.info(f"Skipping {thisFile}, since we already have it.")
            continue

        try:
            with open(thisFile) as f:
                raw = f.read()
        except:
            try:
                with open(thisFile, encoding='latin1') as f:
                    raw = f.read()
            except:
                logging.info(f"Problem with {thisFile}, skipping.") 
                continue

        paras = toParas(raw)
        nParas = len(paras)

        logging.info(f'Disambiguating {nParas} paragraphs...')
        disambiguated = wsd(paras, nlp)

        annotated = annotate(disambiguated)

        with open(outfile, 'w') as f:
            f.write(annotated)
