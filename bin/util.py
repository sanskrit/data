import collections
import csv


def key_fn(x):
    sounds = 'aAiIuUfFxXeEoOMHkKgGNcCjJYwWqQRtTdDnpPbBmyrlLvSzsh|'
    assert all (L in sounds for L in x), x
    return tuple(sounds.index(L) for L in x)


class HashTrie(object):

    """A fast trie, for short items."""

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
        self.splitter = HashTrie()
        for first, second, result in rules:
            result = result.replace(' ', '')
            items = (first, second, result, len(first), len(second),
                     len(result))
            self.splitter[result] = items

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


class read_csv(object):

    def __init__(self, filename, labels=None):
        self.filename = filename
        self.labels = labels

    def __enter__(self):
        self.f = open(self.filename, 'r')
        self.reader = csv.DictReader(self.f, self.labels)
        return self.reader

    def __exit__(self, type, value, traceback):
        self.f.close()


class write_csv(object):

    def __init__(self, filename, labels):
        self.filename = filename
        self.labels = labels

    def __enter__(self):
        self.f = open(self.filename, 'w')
        self.writer = csv.DictWriter(self.f, self.labels)
        self.writer.writeheader()
        return self.writer.writerow

    def __exit__(self, type, value, traceback):
        self.f.close()


def make_csv_string(labels, rows):
    """Print the given data as a CSV.

    :param labels: a list of labels
    :param rows: a list of lists of strings. Each inner list must have
                 a 1:1 correspondence with `labels`.
    """
    data = [','.join(labels)]
    data.extend(','.join([x or '' for x in row]) for row in rows)
    return '\n'.join(data)
