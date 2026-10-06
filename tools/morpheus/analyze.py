#!/usr/bin/env python3
"""
Generate an independent, rule-based morphological analysis of the Apostolic
Fathers with the Morpheus analyzer (the Perseus morphological parser).

For every Greek token this writes the same column layout as `data/morph/`:

  reference  POS  parsing  text  word  normalized  lemma  language  source

where POS/parsing/lemma come from Morpheus (the `source` column is `morpheus`).
This is meant to complement the existing analysis: Morpheus is rule/lexicon
based, so it is a useful cross-check for the machine-generated entries.

Requirements (see tools/morpheus/README.md):
  * a built Morpheus checkout (bin/cruncher), and
  * morpheus-toolkit (Unicode/JSON wrapper + ranking):
      pip install "git+https://github.com/QuantForgeSoftware/morpheus@feature/unicode-toolkit-and-ranking#subdirectory=python"

Usage:
  tools/morpheus/analyze.py --morpheus-dir /path/to/morpheus
  tools/morpheus/analyze.py --morpheus-dir /path/to/morpheus --only data/morph/011-didache.txt
"""
from __future__ import annotations

import argparse
import glob
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

try:
    from morpheus_toolkit import Morpheus
    from morpheus_toolkit.morphgnt import parsing_code, pos_code
except ImportError:
    sys.exit(
        "morpheus-toolkit is not installed. See tools/morpheus/README.md for install "
        "instructions (pip install the python/ subdirectory of the morpheus checkout)."
    )


def analyze_file(morpheus: Morpheus, in_path: str, out_path: str) -> tuple[int, int]:
    rows = []
    with open(in_path, encoding="utf-8") as handle:
        for line in handle:
            fields = line.split()
            if len(fields) < 9 or fields[7] != "grc":
                continue
            rows.append(fields)

    results = morpheus.analyze_tokens([fields[4] for fields in rows])

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    written = 0
    with open(out_path, "w", encoding="utf-8") as out:
        for fields, result in zip(rows, results):
            best = result.best
            if best is None:
                continue
            reference, _, _, text, word, normalized, _, language, _ = fields
            out.write(
                f"{reference} {pos_code(best)} {parsing_code(best)} {text} {word} "
                f"{normalized} {best.lemma} {language} morpheus\n"
            )
            written += 1
    return len(rows), written


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--morpheus-dir", required=True, help="path to a built morpheus checkout")
    parser.add_argument("--only", help="analyze a single input file")
    parser.add_argument("--limit", type=int, default=0, help="limit tokens per file (debugging)")
    args = parser.parse_args()

    # unknown_as_proper gives the many biblical names a synthetic proper-noun
    # analysis instead of leaving them blank.
    morpheus = Morpheus(morpheus_dir=args.morpheus_dir, unknown_as_proper=True)

    inputs = [args.only] if args.only else sorted(glob.glob(os.path.join(REPO, "data", "morph", "*.txt")))
    if not inputs:
        parser.error("no input files found under data/morph/")

    total = analyzed = 0
    for in_path in inputs:
        name = os.path.basename(in_path)
        out_path = os.path.join(REPO, "data", "morph-morpheus", name)
        count, written = analyze_file(morpheus, in_path, out_path)
        total += count
        analyzed += written
        print(f"{name:<30} {written:>6}/{count:<6} tokens  ->  data/morph-morpheus/{name}")
    print(f"\n{analyzed}/{total} Greek tokens analyzed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
