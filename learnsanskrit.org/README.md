Data from learnsanskrit.org
===========================

Hand-constructed data from learnsanskrit.org. Most of the data comes from M. R.
Kale's *A Higher Sanskrit Grammar*.

This folder contains:


The files
---------

### `adjectives-irregular-inflected.csv`

(Headers: `stem,stem_genders,form,form_gender,case,number`)

Irregular adjectives from M. R. Kale's *A Higher Sanskrit Grammar*.


### `nominal-endings-compounded.csv`

(Headers: `stem,stem_genders,form,form_gender`)

Nominal compound forms of various stems. Rows where the stem is `_` correspond
to "ordinary" consonant stems (`vAc`, `-muh`).


### `nominal-endings-inflected.csv`

(Headers: `stem,stem_genders,form,form_gender,case,number`)

Nominal inflectional endings for various stems. Rows where the stem is `_`
correspond to "ordinary" consonant stems (`vAc`, `-muh`).


### `nouns-irregular-inflected.csv`

(Headers: `stem,stem_genders,form,form_gender,case,number`)

Irregular nouns from M. R. Kale's *A Higher Sanskrit Grammar*.


### `pronouns-compounded.csv`

(Headers: `stem,stem_genders,form`)

A list of compounded pronouns.


### `pronouns-inflected.csv`

(Headers: `stem,stem_genders,form,form_gender,case,number`)

A list of inflected pronouns.


### `sandhi-rules.csv`

A list of all sandhi rules that can be described in the form "A + B -> C". This
list excludes sandhi rules that are specific to a single morpheme or a small
set of morphemes.

The list is a CSV file with the following headers:

- `first` is the first part of the combination.
- `second` is the second part of the combination.
- `result` is the result. If `first` changes but `second` does not, the two are
  separated by whitespace.
- `type` is one of `common`, `internal`, or `external`. `common` rules occur in
  all contexts, `internal` rules apply between morphemes (generally speaking),
  and `external` rules apply between words (generally speaking).


### `upasargas.csv`

A list of all upasargas. This excludes other prefixes, such as noun prefixes
(`sa`) and non-upasarga verb prefixes (`svAgatI`).

The list is a CSV file with `name` for a header, where `name` is the upasarga.


### `verb-endings.csv`

(Headers: `form,class,person,number,mode,voice`)

A list of verb endings.


Column types
------------

- `case`: the grammatical case. Possible values:
  - `1` for case 1 (`naras`)
  - `2` for case 2 (`naram`)
  - `3` for case 3 (`nareRa`)
  - `4` for case 4 (`narAya`)
  - `5` for case 5 (`narAt`)
  - `6` for case 6 (`narasya`)
  - `7` for case 7 (`nare`)
  - `8` for case 8 (`nara`)
- `class`: the verb class. Possible values:
  - `simple` for classes 1, 4, 6, and 10 (and denominative verbs)
  - `complex` for classes 2, 3, 5, 7, 8, and 9
  - `both` for any class
- `form`: the form itself (`narasya`).
- `form_gender`: the grammatical gender of the form. Possible values:
  - `m` for masculine (`naras`)
  - `f` for feminine (`vidyA`)
  - `n` for neuter (`Palam`)
  - `none` for non-gendered forms (`aham`)
- `mode`: the verb mode. Possible values:
  - `aor` for the aorist (`agamat`)
  - `ben` for the benedictive (`gamyAt`)
  - `cond` for the conditional (`agamizyat`)
  - `impv` for the imperative (`gacCa`)
  - `inj` for the injunctive (`gamat`)
  - `ipft` for the imperfect (`agacCat`)
  - `opt` for the optative (`gacCet`)
  - `perf` for the perfect (`jagAma`)
  - `pfut` for the periphrastic future (`gantA`)
  - `pres` for the present tense (`gacCati`)
  - `sfut` for the simple future (`gamizyati`)
- `number`: the grammatical number. Possible values:
  - `s` for the singular (`naras`)
  - `d` for the dual (`narau`)
  - `p` for the plural (`narAs`)
- `person`: the verb person. Possible values:
  - `1` for the first person (`gacCAmi`)
  - `2` for the second person (`gacCasi`)
  - `3` for the third person (`gacCati`)
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
- `voice`: the verb voice. Possible values:
  - `atma` for atmanepada
  - `para` for parasmaipada
