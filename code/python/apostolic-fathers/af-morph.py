import os
import regex as re
from dataclasses import dataclass
from greek_normalisation.normalise import Normaliser, Norm
from unicodedata import normalize
import spacy
from spacy.tokens import MorphAnalysis
from morph_maps import *
import requests


@dataclass
class MorphUnit:
    bcv: str
    pos: str
    parse_code: str
    text: str
    word: str
    normalized: str
    lemma: str
    lang: str
    source: str


# MorphGNT SBLGNT
# retrieve directly from git to ensure we get the latest
github_raw = 'https://raw.githubusercontent.com/MorphGNT/sblgnt/master/'
morphgnt_files = ['61-Mt-morphgnt.txt', '62-Mk-morphgnt.txt', '63-Lk-morphgnt.txt', '64-Jn-morphgnt.txt',
                  '65-Ac-morphgnt.txt', '66-Ro-morphgnt.txt', '67-1Co-morphgnt.txt', '68-2Co-morphgnt.txt',
                  '69-Ga-morphgnt.txt', '70-Eph-morphgnt.txt', '71-Php-morphgnt.txt', '72-Col-morphgnt.txt',
                  '73-1Th-morphgnt.txt', '74-2Th-morphgnt.txt', '75-1Ti-morphgnt.txt', '76-2Ti-morphgnt.txt',
                  '77-Tit-morphgnt.txt', '78-Phm-morphgnt.txt', '79-Heb-morphgnt.txt', '80-Jas-morphgnt.txt',
                  '81-1Pe-morphgnt.txt', '82-2Pe-morphgnt.txt', '83-1Jn-morphgnt.txt', '84-2Jn-morphgnt.txt',
                  '85-3Jn-morphgnt.txt', '86-Jud-morphgnt.txt', '87-Re-morphgnt.txt']

# OpenText.org
opentext_dir = "c:/git/OpenText/non_NT_annotation/"

# Apostolic Fathers
apostolic_fathers_dir = "c:/git/jtauber/apostolic-fathers/texts/"

# output dir
output_dir = "c:/git/RickBrannan/apostolic-fathers/data/morph/"

# nlp
greek_model = "grc_proiel_lg"
latin_model = "la_core_web_lg"
nlp = spacy.load(greek_model)
nlp_lat = spacy.load(latin_model)

# first read in morphgnt words
morph_units = {}
word_data = {}
for filename in morphgnt_files:
    print("Processing " + filename)
    abbrev = re.sub(r'\.txt$', '', filename).split('-')[1]
    # open the file as a list of lines
    response = requests.get(github_raw + filename)
    lines = response.text.split('\n')
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        cols = line.split(' ')
        word = normalize('NFKC', cols[5])
        morph = MorphUnit(cols[0], cols[1], cols[2], cols[3], normalize('NFKC', cols[4]), cols[5], cols[6],
                          "grc", "MorphGNT")
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

# pos_map = {}
# pos_map['NOUN'] = 'N-'
# pos_map['VERB'] = 'V-'
# pos_map['ADJ'] = 'A-'
# pos_map['DET'] = 'RA'
# pos_map['ADV'] = 'D-'


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
                line = re.sub(r'  +', ' ', line)
                tokens = line.split(' ')
                bcv = ""
                if book_num != "013":
                    (chapter, verse) = tokens[0].split('.')
                    chapter = chapter.zfill(3)
                    verse = verse.zfill(3)
                    bcv = f"{book_num}{chapter}{verse}"
                else:
                    (section, chapter, verse) = tokens[0].split('.')
                    section = section.zfill(3)
                    chapter = chapter.zfill(3)
                    verse = verse.zfill(3)
                    # determine work from writing
                    work = "000"
                    if int(section) < 6:
                        work = "001" # visions
                    elif int(section) < 18:
                        work = "002" # mandates
                        section = str(int(section) - 5).zfill(3)
                    else:
                        work = "003" # similitudes
                        section = str(int(section) - 17).zfill(3)

                    # this isn't correct, but good enough for now
                    bcv = f"{book_num}{work}{section}{chapter}{verse}"

                # run nlp on the line to get lemmatized word
                # assuming tokens in doc line up with split on space
                doc = nlp(re.sub(r'[.,;()\[\]··;’?:]', '', line))
                doc_lat = nlp_lat(re.sub(r'[.,;()\[\]··;’?:]', '', line))
                # crasis messes stuff up. also, if it is Latin, it could be hosed as well
                if len(doc[1:]) != len(tokens[1:]):
                    print(f"{bcv}: Token count mismatch: {len(doc[1:])} vs {len(tokens[1:])}")
                    for token in doc[1:]:
                        print(f"{token.text} {token.lemma_} {token.pos_} {token.tag_}")

                n = 0
                for token in tokens[1:]:
                    text = normalize("NFKC", token)
                    n += 1
                    if n < len(doc):
                        nlp_token = doc[n]
                    else:
                        nlp_token = doc[-1]
                    nlp_token_lat = doc_lat[n]
                    # removing punctuation does too much (it removes crasis)
                    word = re.sub(r'[.,;()\[\]··;’?:]', '', text)
                    af_counts['total'] += 1
                    if word in word_data:
                        popular_key = lambda x: max(word_data[word], key=word_data[word].get)
                        (pos, parse_code, lemma) = popular_key(word).split('|')
                        auto_morph = convert_morph(nlp_token.morph)
                        # if parse_code != auto_morph:
                        #     if pos == "V-":
                        #         print(f"Mismatch: {word} {pos} {parse_code} {lemma} vs {nlp_token.pos_} {auto_morph} {nlp_token.morph}")
                        morph = MorphUnit(bcv, pos, parse_code, text, word, normalise(word)[0], lemma, "grc", "MorphGNT")
                        af_morph_units.append(morph)
                        af_counts['tagged'] += 1
                    elif re.search(r"[a-z]", word, re.IGNORECASE):
                        af_counts['latin'] += 1
                        if nlp_token_lat.text != word:
                            print(f"Latin mismatch: {bcv} {word} {nlp_token_lat.text}")
                            n += 1 # bump the Latin token
                            # do we want to try and compensate on POS, lemma, and morph?
                        lemma = nlp_token_lat.lemma_
                        if nlp_token_lat.pos_ in pos_map:
                            pos = pos_map[nlp_token_lat.pos_]
                        else:
                            pos = '??'
                            print(f"Unknown LAT pos: {nlp_token_lat.pos_} (from: {bcv} {word})")
                        auto_morph = convert_morph_lat(nlp_token_lat.morph)
                        morph = MorphUnit(bcv, pos, auto_morph, text, word, normalise(word)[0], lemma,
                                          "lat", latin_model)
                        af_morph_units.append(morph)
                    else:
                        lemma = normalize("NFKC", nlp_token.lemma_)
                        if nlp_token.pos_ in pos_map:
                            pos = pos_map[nlp_token.pos_]
                            if re.search(r"^R", pos):
                                pos = get_pronoun_type(pos, nlp_token.morph)
                        else:
                            pos = '??'
                            print(f"Unknown pos: {nlp_token.pos_} (from: {bcv} {word})")
                        if nlp_token.text != word:
                            print(f"Greek mismatch: {bcv} {word} {nlp_token.text}")
                            # n += 1 # bump the token
                        auto_morph = convert_morph(nlp_token.morph)
                        # print(f"Word not found in MorphGNT: {word} (lemma: {lemma}, pos {pos} ({nlp_token.pos_}, morph {morph}))")
                        morph = MorphUnit(bcv, pos, auto_morph, text, word, normalise(word)[0], lemma,
                                          "grc", greek_model)
                        af_morph_units.append(morph)
                        af_counts['untagged'] += 1
                        if morph.normalized not in missed_words:
                            missed_words[morph.normalized] = 0
                        missed_words[morph.normalized] += 1
        # write out the morph units for this book
        with open(output_dir + af_filename, "w", encoding="utf8") as f:
            for morph in af_morph_units:
                f.write(f"{morph.bcv} {morph.pos} {morph.parse_code} {morph.text} {morph.word} {morph.normalized} "
                        f"{morph.lemma} {morph.lang} {morph.source}\n")

# report missed words sorted by frequency
# for key in sorted(missed_words, key=missed_words.get, reverse=True):
#     print(f"{key}\t{missed_words[key]}")

# report book_word_counts
for key in af_counts:
    print(f"{key}\t{af_counts[key]}")
print(f"Unique missed words: {len(missed_words)}")
