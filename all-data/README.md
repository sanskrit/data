Sanskrit data
=============

A collection of Sanskrit linguistic data. For details, see
[the GitHub repo](github).

[github]: http://github.com/sanskrit/data


The files
---------

### `indeclinables.csv`

(Headers: `name`)

Simple (i.e. non-verbal) indeclinables.


### `nominals.csv`

(Headers: `stem,stem_genders`)

Nouns and adjectives.


### `participles.csv`

(Headers: `stem,root,class,mode,voice,modification`)

Unprefixed participles.


### `prefixed-participles.csv` [optional]

(Headers: `stem,root,class,mode,voice,modification`)

Prefixed participles.


### `prefixed-roots.csv`

(Headers: `prefixed-root,prefixes,unprefixed-root,hom`)

Unprefixed verb roots.


### `prefixed-verbal-indeclinables.csv` [optional]

(Headers: `form,root,pos,modification`)

Prefixed verbal indeclinables, i.e. gerunds (`Agamya`) and infinitives
(`Agantum`).


### `prefixed-verbs.csv` [optional]

(Headers: `form,root,class,person,number,mode,voice,modification`)

Prefixed verbs.


### `prefix-groups.csv`

(Headers: `group,prefixes`)

Clusters of verb prefixes, and the prefixes that compose them. This is useful
if you ran `make_data.py` without setting `--make_prefixed_verbals`.


### `pronouns.csv`

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


### `unprefixed-roots.csv`

(Headers: `root,hom,class,voice`)

Unprefixed verb roots.


### `verbal-indeclinables.csv`

(Headers: `form,root,pos,modification`)

Unprefixed verbal indeclinables, i.e. gerunds (`gatvA`) and infinitives
(`gantum`).


### `verb-prefixes.csv`

(Headers: `name,prefix_type`)

Verb prefixes.


### `verbs.csv`

(Headers: `form,root,class,person,number,mode,voice,modification`)

Unprefixed verbs.
