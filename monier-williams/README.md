`monier-williams`
=================

Data from the Monier-Williams Sanskrit-English Dictionary.

The dictionary is large (70 MB) and hosted elsewhere, so it's not included in
the repo. But you can download the dictionary [from the Cologne Digital
Sanskrit Dictionaries project](mw), if you so choose.

[mw]: http://www.sanskrit-lexicon.uni-koeln.de/scans/MWScan/2014/web/webtc/download.html


However, the repo *does* include some supplemental data that can't be
downloaded so easily. This is in the "Greek data" section below.


The files
---------

### `indeclinables.csv`
(Headers: `name`)

Indeclinables, including adverbs, particles (*nipāta*), and more.

### `nominals.csv`
(Headers: `stem,stem_genders`)

Nominal stems, including nouns and adjectives.


Greek data
----------

The dictionary uses a variety of Greek terms. In `monier.xml`, these are
written as `<gk>1</gk>`, `<gk>2</gk>`, and so on. These numbers are indices
into a separate list:

### `greeklist.csv`
The list of Greek terms.

The list is a CSV file with `L,betacode,index` for a header:

- `L` is the unique ID associated with the entry in the dictionary.
- `betacode` is the [Beta Code](betacode) of the original Greek. (Just as
  Sanskrit has Harvard-Kyoto and ITRANS, Greek has Betacode.)
- `index` is the corresponding index.

So if entry `4` contains `<gk>2</gk>`, `2` should be replaced by the
corresponding betacode (in this case, `A)N`).

In retrospect, `L,index,betacode` is a more intuitive order, but it's not
really worth changing.

[betacode]: http://en.wikipedia.org/wiki/Beta_Code


Column types
------------

- `stem`: the stem that produced the form (`nara`).
- `stem_genders`: the grammatical genders of the stem, since a single stem can
  be inflected in multiple genders. Possible values:
  - `m` for masculine (`nara`)
  - `f` for feminine (`vidyA`)
  - `n` for neuter (`Pala`)
  - `mf` for masculine or feminine
  - `fn` for feminine or neuter
  - `mn` for masculine or neuter
  - `mfn` for any gender
  - `none` for non-gendered stems (`mad`)
