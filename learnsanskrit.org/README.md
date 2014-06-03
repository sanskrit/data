Data from learnsanskrit.org
===========================

This folder contains:


`sandhi-rules.csv`
------------------

A list of all sandhi rules that can be described in the form "A + B -> C". This
list excludes sandhi rules that are specific to a single morpheme or a small
set of morphemes.

The list is a CSV file with `first,second,result,type` for a header:

- `first` is the first part of the combination.
- `second` is the second part of the combination.
- `result` is the result. If `first` changes but `second` does not, the two are
  separated by whitespace.
- `type` is one of `common`, `internal`, or `external`. `common` rules occur in
  all contexts, `internal` rules apply between morphemes (generally speaking),
  and `external` rules apply between words (generally speaking).


`upasargas.csv`
---------------

A list of all upasargas. This excludes other prefixes, such as noun-prefixes
("sa") and non-upasarga verb prefixes ("svAgatI").

The list is a CSV file with `name` for a header, where `name` is the upasarga.
