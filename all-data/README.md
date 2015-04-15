Sanskrit data
=============

A collection of Sanskrit linguistic data. For implementation details, see the
project homepage at http://github.com/sanskrit/data .


Different data files are under different licenses, depending on the source that
produced them. The licenses are:

- `MW` for files under the Monier-Williams license.
- `SHS` for files under the Sanskrit Heritage Site license.
- `LSO` for files under the learnsanskrit.org license. (These files are in the
  public domain.)


The files
---------

### `indeclinables.csv` [MW]

(Headers: `name`)

Simple (i.e. non-verbal) indeclinables.


### `nominals.csv` [MW]

(Headers: `stem,stem_genders`)

Nouns and adjectives.


### `nominal-endings-compounded.csv` [LSO]

(Headers: `stem,stem_genders,ending,form_gender`)

Endings for nominals that are in some compound.


### `nominal-endings-inflected.csv` [LSO]

(Headers: `stem,stem_genders,ending,form_gender,case,number`)

Endings for inflected nominals.


### `participles.csv` [SHS]

(Headers: `stem,root,class,mode,voice,modification`)

Unprefixed participles.


### `prefixed-participles.csv` [SHS]

(Headers: `stem,root,class,mode,voice,modification`)

Prefixed participles. If `make_data.py` was run without
`--make_prefixed_verbals`, this file won't appear.


### `prefixed_roots.csv` [MW]

(Headers: `prefixed_root,prefixes,unprefixed_root,hom`)

Unprefixed verb roots.


### `prefixed-verbal-indeclinables.csv` [SHS]

(Headers: `form,root,pos,modification`)

Prefixed verbal indeclinables, i.e. gerunds (`Agamya`) and infinitives
(`Agantum`). If `make_data.py` was run without `--make_prefixed_verbals`, this
file won't appear.


### `prefixed-verbs.csv` [SHS]

(Headers: `form,root,class,person,number,mode,voice,modification`)

Prefixed verbs. If `make_data.py` was run without `--make_prefixed_verbals`,
this file won't appear.


### `prefix-groups.csv` [MW]

(Headers: `group,prefixes`)

Clusters of verb prefixes, and the prefixes that compose them. This is useful
if you ran `make_data.py` without setting `--make_prefixed_verbals`.


### `pronouns.csv` [LSO]

(Headers: `stem,stem_genders,form,form_gender,case,number`)

A list of inflected pronouns.


### `sandhi-rules.csv` [LSO]

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


### `unprefixed_roots.csv` [MW]

(Headers: `root,hom,class,voice`)

Unprefixed verb roots.


### `verbal-indeclinables.csv` [MW]

(Headers: `form,root,pos,modification`)

Unprefixed verbal indeclinables, i.e. gerunds (`gatvA`) and infinitives
(`gantum`).


### `verb-prefixes.csv` [MW]

(Headers: `name,prefix_type`)

Verb prefixes.


### `verbs.csv` [SHS]

(Headers: `form,root,class,person,number,mode,voice,modification`)

Unprefixed verbs.


Column types
------------

- `class`: the verb class. Possible values:
  - `1` for class 1 (`gacCati`)
  - `2` for class 2 (`atti`)
  - `3` for class 3 (`juhoti`)
  - `4` for class 4 (`dIvyati`)
  - `5` for class 5 (`sunoti`)
  - `6` for class 6 (`tudati`)
  - `7` for class 7 (`ruRadDi`)
  - `8` for class 8 (`tanoti`)
  - `9` for class 9 (`krIRAti`)
  - `10` for class 10 (`corayati`)
  - `denom` for denominative verbs (`putrIyati`)
- `hom`: short for *homonym*, this distinguishes two roots that sound the same
  but have different meanings. Possible values are either the empty string or
  a number (e.g. `1`). These come straight from the MW dictionary.
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
- `modification`: the modification (if any) that was applied to the verb.
- `number`: the verb number. Possible values:
  - `s` for the singular (`gacCati`)
  - `d` for the dual (`gacCatas`)
  - `p` for the plural (`gacCanti`)
- `prefix_type`: the type of the verb prefix. Possible values;
  - `cvi` for *cvi* prefixes
  - `DAc` for *ḍāc* prefixes
  - `other` for other prefixes (excluding *upasarga*s)
- `prefixed_root`: a prefixed verb root (`Agam`, but not `gam`)
- `root`: a verb root (`gam`).
- `stem`: a nominal stem (`nara`, `sundara`, `gantavya`)
- `stem_genders`: the grammatical genders of the stem, since a single stem can
  be inflected in multiple genders. Possible values:
  - `m` for masculine (`nara`)
  - `f` for feminine (`vidyA`)
  - `n` for neuter (`Pala`)
  - `mf` for masculine or feminine
  - `fn` for feminine or neuter
  - `mn` for masculine or neuter
  - `mfn` for any gender. This is used for adjectives.
  - `none` for non-gendered stems (`mad`)
- `unprefixed_root`: an unprefixed verb root (`gam`, but not `Agam`)
- `voice`: the verb voice. Possible values:
  - `active` for non-passive. This is useful, e.g., for participle stems like
    `BUtavat`.
  - `atma` for atmanepada
  - `para` for parasmaipada
  - `pass` for passive verbs
