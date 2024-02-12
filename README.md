# apostolic-fathers
 Spot for Rick to put stuff when he's messing with apostolic fathers data

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

Some stats:

* total AF words: 64949
* total tagged words: 52676
* total untagged words: 12273
* total Latin words: 1703
* total unique missed words: 7907

My next step will be to incorporate any morph I can find in the OpenText material (Didache and Diognetus). (**Update:** 
I looked at the OpenText data, and it only has morph and lemma for words that occur in the NT, so ... they took the same shortcut 
I did. So I'm skipping it.

That means I'll use a trained model to knock off some lemmatization and morph. Planning on using 
[this model from HuggingFace](https://huggingface.co/Jacobo/grc_proiel_trf), which
I've dabbled with before for lemma generation. Hoping the morph stuff is decent as well. 

This is _totally_ an in-my-spare-time and as-I-feel-inspiried kind of project. And I don't have a lot of spare time. No promises 
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
 
