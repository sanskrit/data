# -*- coding: utf-8 -*-
"""
    Scrape the Sanskrit Heritace Site for linguistic data.

    :license: MIT and BSD
"""

import sys
import xml.etree.cElementTree as ET


translator = {
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
