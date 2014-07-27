`sanskrit-heritage-site`
========================

Data from the [Sanskrit Heritage Site](http://sanskrit.inria.fr).

The [original data](http://sanskrit.inria.fr/DATA/XML/) is a set of XML
documents:

- `SL_adverbs.xml` for miscellaneous indeclinables.
- `SL_final.xml` for miscellaneous words.
- `SL_nouns.xml` for nouns, adjectives, and numbers.
- `SL_parts.xml` for inflected participles.
- `SL_pronouns.xml` for pronoun data.
- `SL_roots.xml` for inflected verbs.

`SL_nouns.xml`, `SL_pronouns`, and parts of `SL_adverbs.xml` and `SL_final.xml`
are superseded by the data in the other folders. So, this folder contains the
following data instead:

The files
---------
### `adverbs.csv`
(Headers: `name,root,pos,modification`)

`-tvA` gerunds. This file was generated from `SL_adverbs.xml`.

### `final.csv`
(Headers: `name,root,pos,modification`)

Infinitives and `-ya` gerunds. This file was generated from `SL_final.xml`.

### `roots.csv`
(Headers: `name,root,class,person,number,mode,voice,modification`)

Inflected verbs. This file was generated from `SL_roots.xml`.

Column types
------------

- `name`: the form itself (`gacCati`).
- `root`: the root that produced the form (`gam`). This uses the Sanskrit
  Heritage Site notation.
- `pos`: the part-of-speech. Possible values:
  - `gerund` for gerunds
  - `infinitive` for infinitives
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
- `person`: the verb person. Possible values:
  - `1` for the first person (`gacCAmi`)
  - `2` for the second person (`gacCasi`)
  - `3` for the third person (`gacCati`)
- `number`: the verb number. Possible values:
  - `s` for the singular (`gacCati`)
  - `d` for the dual (`gacCatas`)
  - `p` for the plural (`gacCanti`)
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
- `voice`: the verb voice. Possible values:
  - `atma` for atmanepada
  - `para` for parasmaipada
  - `pass` for passive verbs
- `modification`: the modification (if any) that was applied to the verb.
  Possible values:
  - `caus` for causative (`gamayati`)
  - `desid` for desiderative (`jigamizati`)
  - `intens` for intensives (`jaNgamyate`)
