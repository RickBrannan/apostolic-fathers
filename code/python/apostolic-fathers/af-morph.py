import os
import regex as re
from dataclasses import dataclass
from greek_normalisation.normalise import Normaliser, Norm
from unicodedata import normalize
import spacy
from spacy.tokens import MorphAnalysis
from morph_maps import *


@dataclass
class MorphUnit:
    bcv: str
    pos: str
    parse_code: str
    text: str
    word: str
    normalized: str
    lemma: str


# MorphGNT SBLGNT
morphgnt_dir = "c:/git/MorphGNT/sblgnt/"

# OpenText.org
opentext_dir = "c:/git/OpenText/non_NT_annotation/"

# Apostolic Fathers
apostolic_fathers_dir = "c:/git/jtauber/apostolic-fathers/texts/"

# output dir
output_dir = "c:/git/RickBrannan/apostolic-fathers/data/morph/"

# nlp
nlp = spacy.load("grc_proiel_sm")

# first read in morphgnt words
morph_units = {}
word_data = {}
for filename in os.listdir(morphgnt_dir):
    if filename.endswith(".txt"):
        print("Processing " + filename)
        abbrev = re.sub(r'\.txt$', '', filename).split('-')[1]
        # open the file as a list of lines
        # since it is one line per word, this gives word count.
        with open(morphgnt_dir + filename, encoding="utf8") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                cols = line.split(' ')
                word = normalize('NFKC', cols[5])
                morph = MorphUnit(cols[0], cols[1], cols[2], cols[3], normalize('NFKC', cols[4]), cols[5], cols[6])
                morph_units[morph.bcv] = morph
                if morph.word not in word_data:
                    word_data[morph.word] = {}
                key = f"{morph.pos}|{morph.parse_code}|{morph.lemma}"
                if key not in word_data[morph.word]:
                    word_data[morph.word][key] = 0
                word_data[morph.word][key] += 1

# ok, let's read us some AF and slap some very provisional data together.
normalise = Normaliser().normalise
af_counts = {}
af_counts['total'] = 0
af_counts['tagged'] = 0
af_counts['untagged'] = 0
af_counts['latin'] = 0
missed_words = {}

pos_map = {}
pos_map['NOUN'] = 'N-'
pos_map['VERB'] = 'V-'
pos_map['ADJ'] = 'A-'
pos_map['DET'] = 'RA'
pos_map['ADV'] = 'D-'


for af_filename in os.listdir(apostolic_fathers_dir):
    if af_filename.endswith(".txt"):
        print("Processing " + af_filename)
        af_morph_units = []
        # remove first four chars and .txt extension
        book_num = re.sub(r'^(\d{3}).*$', r'\1', af_filename)
        # skip the shepherd, for now
        # if book_num == '013':
        #     continue
        # open the file as a list of lines
        with open(apostolic_fathers_dir + af_filename, encoding="utf8") as f:
            for line in f.readlines():
                # each line is a verse
                # remove leading and trailing whitespace
                line = line.strip()
                tokens = line.split(' ')
                bcv = ""
                if book_num != "013":
                    (chapter, verse) = tokens[0].split('.')
                    chapter = chapter.zfill(3)
                    verse = verse.zfill(3)
                    bcv = f"{book_num}{chapter}{verse}"
                else:
                    (writing, chapter, verse) = tokens[0].split('.')
                    writing = writing.zfill(3)
                    chapter = chapter.zfill(3)
                    verse = verse.zfill(3)
                    bcv = f"{book_num}{writing}{chapter}{verse}"

                # run nlp on the line to get lemmatized word
                # assuming tokens in doc line up with split on space
                doc = nlp(re.sub(r'[.,;()\[\]··;’]', '', line))
                if len(doc[1:]) != len(tokens[1:]):
                    print(f"{bcv}: Token count mismatch: {len(doc[1:])} vs {len(tokens[1:])}")
                    for token in doc[1:]:
                        print(f"{token.text} {token.lemma_} {token.pos_} {token.tag_}")

                n = 0
                for token in tokens[1:]:
                    text = normalize("NFKC", token)
                    n += 1
                    nlp_token = doc[n]
                    # removing punctuation does too much (it removes crasis)
                    word = re.sub(r'[.,;()\[\]·]', '', text)
                    af_counts['total'] += 1
                    if word in word_data:
                        popular_key = lambda x: max(word_data[word], key=word_data[word].get)
                        (pos, parse_code, lemma) = popular_key(word).split('|')
                        auto_morph = convert_morph(nlp_token.morph)
                        if parse_code == auto_morph:
                            print(f"Match: {word} {pos} {parse_code} {lemma}")
                        else:
                            print(f"Mismatch: {word} {pos} {parse_code} {lemma} vs {nlp_token.pos_} {auto_morph}")
                        morph = MorphUnit(bcv, pos, parse_code, text, word, normalise(word)[0], lemma)
                        af_morph_units.append(morph)
                        af_counts['tagged'] += 1
                    else:
                        lemma = normalize("NFKC", nlp_token.lemma_)
                        if nlp_token.pos_ in pos_map:
                            pos = pos_map[nlp_token.pos_]
                            if re.search(r"^R", pos):
                                pos = get_pronoun_type(pos, nlp_token.morph)
                        else:
                            pos = '??'
                        auto_morph = convert_morph(nlp_token.morph)
                        print(f"Word not found in MorphGNT: {word} (lemma: {lemma}, pos {pos} ({nlp_token.pos_}, morph {morph}))")
                        morph = MorphUnit(bcv, pos, auto_morph, text, word, normalise(word)[0], lemma)
                        af_morph_units.append(morph)
                        af_counts['untagged'] += 1
                        if re.search(r"^[a-z]+$", morph.normalized, re.IGNORECASE):
                            af_counts['latin'] += 1
                        if morph.normalized not in missed_words:
                            missed_words[morph.normalized] = 0
                        missed_words[morph.normalized] += 1
        # write out the morph units for this book
        with open(output_dir + af_filename, "w", encoding="utf8") as f:
            for morph in af_morph_units:
                f.write(f"{morph.bcv} {morph.pos} {morph.parse_code} {morph.text} {morph.word} {morph.normalized} {morph.lemma}\n")

# report missed words sorted by frequency
for key in sorted(missed_words, key=missed_words.get, reverse=True):
    print(f"{key}\t{missed_words[key]}")

# report book_word_counts
for key in af_counts:
    print(f"{key}\t{af_counts[key]}")
print(f"Unique missed words: {len(missed_words)}")
