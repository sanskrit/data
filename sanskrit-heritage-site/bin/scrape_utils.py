# -*- coding: utf-8 -*-
"""
    Scrape the Sanskrit Heritace Site for linguistic data.

    :license: MIT and BSD
"""

import sys
import xml.etree.cElementTree as ET


translator = {
    # Gender
    'mas': 'm',
    'fem': 'f',
    'neu': 'n',
    # Case
    'nom': '1',
    'acc': '2',
    'ins': '3',
    'dat': '4',
    'abl': '5',
    'gen': '6',
    'loc': '7',
    'voc': '8',
    # Person
    'fst': '1',
    'snd': '2',
    'trd': '3',
    # Number
    'sg': 's',
    'du': 'd',
    'pl': 'p',
    # Mode
    'ip': 'impv',
    'im': 'ipft',
    'pr': 'pres',
    'op': 'opt',
    'fut': 'sfut',
    'aor': 'aor',
    'cnd': 'cond',
    'pass': 'pass',
    'pef': 'pfut',
    'prf': 'perf',
    'inj': 'inj',
    'ben': 'ben',
    # Voice
    'para': 'para',
    'atma': 'atma',
    'pas': 'pass',
    # Modification
    'prim': None,
    'ca': 'caus',
    'int': 'intens',
    'des': 'desid',
}


def iter_xml(filename):
    """Iterate over each XML row in the given file."""
    with open(filename, 'r') as f:
        for line in f:
            try:
                yield ET.fromstring(line)
            except ET.ParseError:
                pass

def make_csv_string(labels, rows):
    """Print the given data as a CSV
    :param labels: a list of labels
    :param rows: a list of lists of strings. Each inner list must have
                 a 1:1 correspondence with `labels`.
    """
    data = [','.join(labels)]
    data.extend(','.join([x or '' for x in row]) for row in rows)
    return '\n'.join(data)
