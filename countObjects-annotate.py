from nltk.corpus import wordnet as wn
from collections import Counter
import argparse
import logging
import json
from ewiser.spacy.disambiguate import Disambiguator
import spacy
import glob

logging.basicConfig(level=logging.INFO)


def wsdWarmup():
    wsd = Disambiguator('../ewiser/bin/ewiser.semcor+wngt.pt', lang='en',
                batch_size=5, save_wsd_details=False).eval()
    wsd = wsd.to('cpu')
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
    allFiles = glob.glob(directory + "/*")

    logging.info(f"Analyzing files {allFiles}")

    logging.info("Warming up WSD...")
    nlp = wsdWarmup()


    for thisFile in allFiles:
        logging.info(f"Now analyzing file {thisFile}")
        with open(thisFile) as f:
            raw = f.read()

        paras = toParas(raw)[:5]
        nParas = len(paras)

        logging.info(f'Disambiguating {nParas} paragraphs...')
        disambiguated = wsd(paras, nlp)

        annotated = annotate(disambiguated)

        basename = thisFile.split("/")[-1]
        with open(f"results-cenlab/{basename}-annotated.txt", 'w') as f:
            f.write(annotated)
        exit()
