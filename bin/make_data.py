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


def write_to_output_dir(in_path, outfile):
    """Copy `in_path` to `OUTPUT_DIR`/`outfile`."""
    shutil.copy(in_path, os.path.join(OUTPUT_DIR, outfile))


def write_verb_prefixes(upasargas=None, other=None):
    pass


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

    # Sandhi rules
    write_to_output_dir(paths['lso-sandhi-rules'], 'sandhi-rules.csv')


if __name__ == '__main__':
    main()
