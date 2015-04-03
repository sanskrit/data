# -*- coding: utf-8 -*-
"""
    Code for handling sandhi.

    Most of this code was copied verbatim from the `sanskrit` package.
    It's duplicated here so that all of the data generation code is
    self-contained and hermetic.
"""

import collections


PREFIX_SANDHI_RULES = [
    ('a', 'f', 'Ar'),
    ('i', 's', 'iz'),
    ('i', 'st', 'izw'),
    ('i', 'sT', 'izW'),
    ('u', 's', 'uz'),
    ('u', 'st', 'uzw'),
    ('u', 'sT', 'uzW'),
    ('is', 't', 'izw'),
    ('t', 'sk', 'tk'),
    ('t', 'st', 'tt'),
    ('t', 'sT', 'tT'),
]


class HashTrie(object):

    """A fast trie, for short items.

    Copied from the `sanskrit` package."""

    def __init__(self):
        self.mapper = collections.defaultdict(set)
        self.len_longest = 0
        self.lengths = range(1, self.len_longest + 1)

    def __getitem__(self, key):
        return set.union(*[self.mapper[key[:i]] for i in self.lengths])

    def __setitem__(self, key, value):
        self.mapper[key].add(value)
        self.len_longest = max(len(key), self.len_longest)
        self.lengths = range(1, self.len_longest + 1)


class Sandhi(object):

    """Undoes sandhi rules. Copied from the `sanskrit` package."""

    def __init__(self, rules):
        self.joiner = {}
        self.splitter = HashTrie()

        for first, second, result in rules:
            self.joiner[(first, second)] = result

            result = result.replace(' ', '')
            items = (first, second, result, len(first), len(second),
                     len(result))
            self.splitter[result] = items

    @staticmethod
    def internal_retroflex(term):
        """Apply the "n -> ṇ" and "s -> ṣ" rules of internal sandhi.
        :param term: the term to process
        """
        # causes "s" retroflexion
        s_trigger = set('iIuUfFeEoOkr')
        # causes "n" retroflexion
        n_trigger = set('fFrz')
        # Allowed after n_trigger
        n_between = sounds.VOWELS.union('kKgGNpPbBmhvyM')
        # Must appear after the retroflexed "n"
        n_after = sounds.VOWELS.union('myvn')
        # Defines t retroflexion
        retroflexion_dict = dict(zip('tT', 'wW'))

        letters = list(term)

        apply_s = False
        apply_n = False
        had_n = False  # Used for double retroflexion ('nisanna' -> 'nizaRRa')
        had_s = False  # Used for 't' retroflexion
        for i, L in enumerate(letters[:-1]):
            # "t" retroflexion after "s" retroflexion
            if had_s:
                had_s = False
                letters[i] = retroflexion_dict.get(L, L)

            # "s" retroflexion
            if apply_s and L == 's':
                letters[i] = L = 'z'
                had_s = True
            apply_s = L in s_trigger

            # "n" retroflexion
            if had_n and L == 'n':
                letters[i] = 'R'
                had_n = False
            elif apply_n and L == 'n' and letters[i + 1] in n_after:
                letters[i] = 'R'
                had_n = True
            if L in n_trigger:
                apply_n = True
            else:
                apply_n = apply_n and L in n_between

        return ''.join(letters)

    def join(self, chunks):
        it = iter(chunks)
        returned = next(it)
        for chunk in it:
            # `i` controls the number of letters to grab from the end of
            # the first word. For most rules, one letter is sufficient.
            # But visarga sandhi needs slightly more context.
            for i in (2, 1, 0):
                if not i:
                    returned += chunk
                    break
                key = (returned[-i:], chunk[0])
                result = self.joiner.get(key, None)
                if result:
                    returned = returned[:-i] + result + chunk[1:]
                    break
        return Sandhi.internal_retroflex(returned)

    def splits(self, chunk):
        """Return a generator for all splits in `chunk`. Results are yielded
        as 2-tuples containing the term before the split and the term after::
            for item in s.splits('nareti'):
                before, after = item
        :meth:`splits` will generate many false positives, usually when the
        first part of the split ends in an invalid consonant::
            assert ('narAv', 'iti') in s.splits('narAviti')
        These should be filtered out in the calling function.
        Splits are generated from left to right, but the function makes no
        guarantees on when certain rules are applied. That is, output is
        loosely ordered but nondeterministic.
        """

        splitter = self.splitter
        chunk_len = len(chunk)

        for i in xrange(chunk_len):
            # Default split: chop the chunk in half with no other changes.
            # This can yield a lot of false positives.
            chunk1, chunk2 = chunk[:i], chunk[i:]
            if i:
                yield (chunk1, chunk2)

            # Rule-based splits: undo a sandhi change
            rules = splitter[chunk2]
            for first, second, result, _, _, len_result in rules:
                before = chunk1 + first
                after = second + chunk2[len_result:]
                yield (before, after)

        # Non-split: yield the chunk as-is.
        yield (chunk, '')

    def split_off(self, chunk, fragment):
        """Remove `fragment` from the end of `chunk` and yield the results.
        If `fragment` cannot be found, yield nothing.
        :param chunk: the phrase to split
        :param fragment: the phrase to split off
        """
        for before, after in self.splits(chunk):
            if after == fragment:
                yield before
