import os
import re

# find book word counts for both NT and Apostolic Fathers
# in order to compare

# MorphGNT SBLGNT
morphgnt_dir = "c:/git/MorphGNT/sblgnt/"

# Apostolic Fathers
apostolic_fathers_dir = "c:/git/jtauber/apostolic-fathers/texts/"

# output dir
output_dir = "c:/git/RickBrannan/apostolic-fathers/data/tsv/"

book_word_counts = {}

for filename in os.listdir(morphgnt_dir):
    if filename.endswith(".txt"):
        print("Processing " + filename)
        abbrev = re.sub(r'\.txt$', '', filename).split('-')[1]
        # open the file as a list of lines
        # since it is one line per word, this gives word count.
        with open(morphgnt_dir + filename, encoding="utf8") as f:
            lines = f.readlines()
            book_word_counts[abbrev] = len(lines)

for filename in os.listdir(apostolic_fathers_dir):
    if filename.endswith(".txt"):
        print("Processing " + filename)
        # remove first four chars and .txt extension
        abbrev = re.sub(r'^\d{3}-', '', filename).split('.')[0]
        # open the file as a list of lines
        book_word_count = 0
        with open(apostolic_fathers_dir + filename, encoding="utf8") as f:
            for line in f.readlines():
                # remove leading and trailing whitespace
                line = line.strip()
                # remove punctuation
                line = re.sub(r'^[\d.]+ ', '', line)
                # split on spaces to get word count
                book_word_count += len(line.split(' '))
            book_word_counts[abbrev] = book_word_count

# report book_word_counts
with open(output_dir + "book_word_counts.txt", "w") as f:
    for book in book_word_counts:
        print(book + "\t " + str(book_word_counts[book]))
        f.write(book + "\t " + str(book_word_counts[book]) + "\n")