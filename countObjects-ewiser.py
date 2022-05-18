from nltk.corpus import wordnet as wn
from collections import Counter
import argparse
import logging
import json
from ewiser.spacy.disambiguate import Disambiguator
import spacy

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


def isArtifact(lemma):
    return artifact in [item[0] for item in lemma.hypernym_distances()]


def getArtifacts(disambiguated):
    logging.info(f'Extracting artifacts...')
    artifacts = []
    for i, para in enumerate(disambiguated):
        for word in para:
            if len(word) > 1:
                if word._.offset:
                    if isArtifact(word._.synset):
                        artifacts.append((i, word.i, word, word._.synset))
    return artifacts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count the number of artifacts in a text, according to their WordNet categories.")
    parser.add_argument('filename')
    parser.add_argument('--verbose', action='store_true', help="Print out everything")
    args = parser.parse_args()
    fn = args.filename
    logging.info(f"Reading file {fn}")

    with open(fn) as f:
        raw = f.read()

    logging.info("Warming up WSD...")
    nlp = wsdWarmup()

    paras = toParas(raw)
    nParas = len(paras)

    logging.info(f'Disambiguating {nParas} paragraphs...')
    disambiguated = wsd(paras, nlp)

    logging.info(f'Counting artifacts ...')
    artifact = wn.synsets('object')[0]
    # print(artifact)
    artifacts = getArtifacts(disambiguated)

    if args.verbose:
        print(artifacts)

    artifactSyns = [item[3].name() for item in artifacts]
    counter = Counter(artifactSyns).most_common(40)
    logging.info(f"Total artifacts: {len(artifacts)}")
    out = json.dumps({fn: dict(counter)})
    print(out)
