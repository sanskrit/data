# -*- coding: utf-8 -*-
"""
    make_data
    ~~~~~~~~~

    Combine the various data sources into a single set of CSVs.
"""


import csv
import os
import shutil
import sys
import time

import util

BIN_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.dirname(BIN_DIR)
OUTPUT_DIR = os.path.join(DATA_DIR, 'all-data')


def make_path_map(pairs):
    """Make a map from shorthand names to file paths."""
    paths = {}

    for abbr, prefix in pairs:
        directory = os.path.join(DATA_DIR, prefix)
        for filename in os.listdir(directory):
            if filename.endswith('csv'):
                name = abbr + '-' + os.path.splitext(filename)[0]
                paths[name] = '{}/{}'.format(directory, filename)
    return paths


def get_output_path(filename):
    return os.path.join(OUTPUT_DIR, filename)


def write_to_output_dir(in_path, outfile):
    """Copy `in_path` to `OUTPUT_DIR`/`outfile`."""
    shutil.copy(in_path, get_output_path(outlife))


def write_verb_prefixes(upasargas=None, other=None):
    pass


def get_mw_root_from_shs_root(root, blacklist, override):
    if root in blacklist:
        return None

    if root in override:
        return override[root]

    return root.partition('#')[0]


def write_verbs(data_path, blacklist_path, override_path):
    """

    :param data_path: path to the actual verb data
    :param blacklist_path: path to a list of blacklisted roots
    :param override_path: path to a map from SHS roots to MW roots. If a root
                          isn't in this map, assume the SHS roots are just fine.
    """
    with util.read_csv(blacklist_path) as reader:
        blacklist = {x['name'] for x in reader}

    with util.read_csv(override_path) as reader:
        override = {x['shs']: x['mw'] for x in reader}

    labels = None
    clean_rows = []
    with util.read_csv(data_path) as reader:
        for row in reader:
            root = get_mw_root_from_shs_root(row['root'], blacklist=blacklist,
                                             override=override)
            if root is None:
                continue
            row['root'] = root
            clean_rows.append(row)
        labels = reader.fieldnames

    with util.write_csv(get_output_path('verbs.csv'), labels) as write_row:
        for row in clean_rows:
            write_row(row)


def main():
    paths = make_path_map(
        [('mw', 'monier-williams'),
         ('shs', 'sanskrit-heritage-site'),
         ('lso', 'learnsanskrit.org')])

    # Nouns, pronouns, and adjectives
    write_to_output_dir(paths['mw-nominals'], 'nominals.csv')
    write_to_output_dir(paths['lso-pronouns-inflected'], 'pronouns.csv')

    # Simple indeclinables
    write_to_output_dir(paths['mw-indeclinables'], 'indeclinables.csv')

    # Verb prefixes
    write_verb_prefixes(upasargas=paths['lso-upasargas'],
                        other=paths['mw-verb-prefixes'])

    # Verbs
    write_verbs(data_path=paths['shs-roots'],
                override_path=paths['shs-root-override'],
                blacklist_path=paths['shs-root-blacklist'])

    # Sandhi rules
    write_to_output_dir(paths['lso-sandhi-rules'], 'sandhi-rules.csv')


if __name__ == '__main__':
    main()
