sanskrit-data
=============

Versioned and high-quality Sanskrit linguistic data.

The data has been cobbled together from a variety of sources, each with its own
gaps. The data from the Sanskrit Heritage Site is the least accurate, mainly
because it was generated programmatically.

About the data
--------------
Verbs, participles, nouns, adjectives, pronouns, indeclinables, morphemes, and
sandhi rules. If it's a Sanskrit word, it's probably here.

The data comes from several sources, each with its own license. Check the
LICENSE files in `learnsanskrit.org`, `sanskrit-heritage-site`, and
`monier-williams` for details.

All Sanskrit strings are written in [SLP1](slp1), mainly because it is
*extremely* convenient when processing Sanskrit programmatically. You can
transliterate this data to some other representation by using a variety of
[transliterators](https://github.com/sanskrit/sanscript).

[slp1]: http://sanskrit1.ccv.brown.edu/Sanskrit/Vyakarana/Dhatupatha/mdhvcanidx/disp1/encodinghelp.html

Quickstart
----------
The data comes from several sources, each with its own format. This script
converts all of the data to a common format and stores the results in
the `all-data` folder.

    python bin/make_data.py

... that is, it *will* soon, when it's ready.
