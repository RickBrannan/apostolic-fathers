# Morpheus analysis

An independent, **rule/lexicon-based** morphological analysis of the Apostolic
Fathers, produced with [Morpheus](https://github.com/QuantForgeSoftware/morpheus)
(the morphological parser originally written for the Perseus Project).

The existing `data/morph/` analysis is partly machine-generated
(`grc_proiel_lg`) for forms not found in the Greek New Testament. Morpheus is a
different kind of analyzer — a hand-built stem/ending lexicon — so it provides a
useful cross-check, especially for the non-NT vocabulary.

## Method

1. Build Morpheus (`scripts/build.sh` in the Morpheus checkout).
2. Convert each Unicode token to beta code and run `cruncher`.
3. Rank the candidate analyses by lemma frequency (the bundled table is derived
   from the MorphGNT SBLGNT); Morpheus otherwise orders candidates alphabetically
   by lemma, which often puts the wrong reading first.
4. Map the chosen analysis to the MorphGNT/CCAT POS + parsing codes used here.
5. Give tokens Morpheus cannot analyze (mostly biblical proper names) a synthetic
   proper-noun analysis, so no token is left blank.

The wrapper is [morpheus-toolkit](https://github.com/QuantForgeSoftware/morpheus/tree/feature/unicode-toolkit-and-ranking/python).

## Files

`data/morph-morpheus/*.txt` mirrors `data/morph/*.txt` (Greek tokens only) in the
same column layout:

```
reference  POS  parsing  text  word  normalized  lemma  language  source
```

The `source` column is `morpheus`. Latin portions of the corpus are omitted (only
Greek is analyzed).

## Reproduce

```bash
# 1. Morpheus + toolkit
git clone https://github.com/QuantForgeSoftware/morpheus
cd morpheus && scripts/build.sh && cd ..
pip install "git+https://github.com/QuantForgeSoftware/morpheus@feature/unicode-toolkit-and-ranking#subdirectory=python"

# 2. Generate
tools/morpheus/analyze.py --morpheus-dir /path/to/morpheus
```

## Agreement with `data/morph/`

Measured with `scripts/agreement_report.py` from the Morpheus checkout (gold =
the existing lemma; "coverage" = the gold lemma is among Morpheus's candidates):

| subset | tokens | coverage | top-1 lemma (Morpheus order → ranked) |
| --- | ---: | ---: | ---: |
| all Greek | 63,222 | 90.9% | 84.5% → 89.9% |
| `source=MorphGNT` | 52,094 | 96.4% | 89.7% → 95.7% |
| `source=grc_proiel_lg` | 11,128 | 65.4% | 60.5% → 62.9% |

With the proper-name fallback every Greek token receives an analysis (100%).

## License / provenance

- Morpheus is licensed **MPL-2.0** (Perseus Project; see the Morpheus `LICENSE`).
- `morpheus-toolkit` is MIT.
- The generated analysis files are offered under the same **CC-BY-SA 4.0** terms
  as the rest of `data/`, with attribution to the Perseus Project.
