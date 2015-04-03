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


### `participles.csv` [SHS]

(Headers: `stem,root,class,mode,voice,modification`)

Unprefixed participles.


### `prefixed-participles.csv` [SHS]

(Headers: `stem,root,class,mode,voice,modification`)

Prefixed participles. If `make_data.py` was run without
`--make_prefixed_verbals`, this file won't appear.


### `prefixed-roots.csv` [MW]

(Headers: `prefixed-root,prefixes,unprefixed-root,hom`)

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


### `unprefixed-roots.csv` [MW]

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
