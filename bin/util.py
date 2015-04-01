import collections
import csv


def key_fn(x):
    sounds = 'aAiIuUfFxXeEoOMHkKgGNcCjJYwWqQRtTdDnpPbBmyrlLvSzsh|'
    assert all (L in sounds for L in x), x
    return tuple(sounds.index(L) for L in x)


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
