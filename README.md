# apostolic-fathers
An effort at a freely-available, open-source edition of the Apostolic Fathers with morphology and lemmas.

Initially focused on Greek, but I eventually want to get the Latin portions annotated as well.

## License
This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).

## Apostolic Fathers Greek Morphology

Since there is no publicly available and openly licensed morphology of the writings of the Apostolic Fathers 
(that I know of [besides some stuff from OpenText](https://github.com/OpenText-org/non_NT_annotation); please 
correct me if I'm wrong and supply me links), I figured it was time to start on a project.

I'm starting with James Tauber and Seumas MacDonald's [Open Apostolic Fathers](https://github.com/jtauber/apostolic-fathers).
This is an edition of Kirsopp Lake's edition of the Apostolic Fathers, and is serviceable for these purposes.

In typical Rick fashion, I'm starting with the stupidest thing that might work, and that means mooching off of Tauber's other
project, [MorphGNT](https://github.com/MorphGNT). Like it is so stupid. I'm just taking forms that happen in the Greek NT (SBLGNT) and 
migrating the morph data over to the Apostolic Fathers based on (normalized) word matches.

The output currently mimicks the record style of MorphGNT. If I haven't got the value yet, I just insert `??` as appropriate.

You can find it here:

* data: https://github.com/RickBrannan/apostolic-fathers/tree/main/data/morph/
* code: https://github.com/RickBrannan/apostolic-fathers/tree/main/code/python/apostolic-fathers/af-morph.py

## Current Status

I'm using [this model from HuggingFace](https://huggingface.co/Jacobo/grc_proiel_lg), which
I've dabbled with before for lemma generation. I'm going to initially use the lemma and morph capabilities,
but it has some named entity recognition capabilities as well that I'd like to play around with.

For Greek words unknown by Tauber's MorphGNT, I am now using the `grc_proiel_lg` form of the model to 
include lemmas and morph. These are untested and not reviewed. I've done some comparisons of words known
by MorphGNT against the morph generated for them and found agreement, but it isn't perfect. Some known areas
of trouble include:

* **Crasis.** The model splits a crasis like καγω into two tokens, whereas MorphGNT treats it as one. These are currently causing some problems.
* **Morph mismatches.** The model doesn't emit morphology as traditionally thought of by most Koine/Hellenistic Greek Grammars. For example,
the model has tense values of past, present, and future along with Aspect values of perfective and imperfective. I'm unsure how well this 
data can be combined to map over to include as 'tense' stuff like aorist, perfect, imperfect, and pluperfect. But we'll see.
* **Shepherd identifiers.** The identifiers for the Shepherd follow the Open Apostolic Fathers, which count the highest level from start to finish instead of
starting over at each major section (Visions, Mandates, Similitudes), so there is no easy way to map to known citation systems. I'll correct this 
sometime, it isn't important (yet) to getting the morph in.

All that said, there is data now available that has some sort of (unproven, untested, and wrong in spots) morphology for
almost every available token.

*Disclaimer:* This is _totally_ an in-my-spare-time and as-I-feel-inspiried kind of project. And I don't have a lot of spare time. No promises 
about status and finishing, use at your own risk, etc.

### Columns

 * book/chapter/verse
   * unlike MorphGNT, I use three digit fields as the Shepherd has over 100 chapters.
   * unlike MorphGNT, the Shepherd has four values: book/writing/chapter/verse. However I plan to migrate them to Whittaker's chapter-verse structure.
 * part of speech
 * parsing code
 * text (including punctuation)
 * word (with punctuation stripped)
 * normalized word (using Tauber's `greek_normalisation` Python library
 * lemma

### Part of Speech Code

* A- adjective  
* C- conjunction  
* D- adverb  
* I- interjection  
* N- noun  
* P- preposition  
* RA definite article  
* RD demonstrative pronoun  
* RI interrogative/indefinite pronoun  
* RP personal pronoun  
* RR relative pronoun  
* V- verb  
* X- particle  

### Parsing Code

 * person (1=1st, 2=2nd, 3=3rd)
 * tense (P=present, I=imperfect, F=future, A=aorist, X=perfect, Y=pluperfect)
 * voice (A=active, M=middle, P=passive)
 * mood (I=indicative, D=imperative, S=subjunctive, O=optative, N=infinitive, P=participle)
 * case (N=nominative, G=genitive, D=dative, A=accusative)
 * number (S=singular, P=plural)
 * gender (M=masculine, F=feminine, N=neuter)
 * degree (C=comparative, S=superlative)
 
