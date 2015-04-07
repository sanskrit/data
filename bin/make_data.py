# -*- coding: utf-8 -*-
"""
    make_data
    ~~~~~~~~~

    Combine the various data sources into a single set of CSVs.
"""


import argparse
import csv
import os
import Queue
import shutil
import sys
import time

import sandhi as S
import util


parser = argparse.ArgumentParser(description='Generates usable Sanskrit data.')
parser.add_argument('--make_prefixed_verbals', action='store_true',
                    help="If set, generate prefixed verbals " +
                    "('AgacCati', 'Agata', 'Agantum').")


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
                name = abbr + '/' + os.path.splitext(filename)[0]
                paths[name] = '{}/{}'.format(directory, filename)
    return paths


def get_output_path(filename):
    return os.path.join(OUTPUT_DIR, filename)


def copy_to_output_dir(in_path, out_path):
    """Copy `in_path` to `out_path`."""
    shutil.copy(in_path, out_path)


def make_sandhi_object(sandhi_rules_file):
    """Makes a Sandhi object for splitting and joining verb prefixes."""
    with util.read_csv(sandhi_rules_file) as reader:
        rules = [(x['first'], x['second'], x['result']) for x in reader]
        return S.Sandhi(rules + S.PREFIX_SANDHI_RULES)


def write_verb_prefixes(upasargas, other, out_path):
    with util.read_csv(upasargas) as reader:
        upasargas = list(reader)

    with util.read_csv(other) as reader:
        other = list(reader)
        labels = reader.fieldnames

    assert 'prefix_type' in labels
    for x in upasargas:
        assert 'prefix_type' not in x
        x['prefix_type'] = 'upasarga'

    rows = sorted(upasargas + other, key=lambda x: util.key_fn(x['name']))
    with util.write_csv(out_path, labels) as write_row:
        for row in rows:
            write_row(row)


def write_prefix_groups(prefixed_roots, unprefixed_roots, upasargas, other,
                        sandhi_rules, out_path):
    """Parse the prefixes in a prefix root and write out the prefix groups.

    The procedure is roughly as follows:

        for each prefixed root in `prefixed_roots`:
            find (p_1, ..., p_n, r), where p_x is a prefix and r is a root
            write the prefix group (p_1, ..., p_n) to file.

    We find (p_1, .., p_n) by using the rules in `sandhi_rules` and verify
    that `p_x` is a prefix by checking for membership in `upasargas` and
    `other`.
    """

    # Loading prefixes
    all_prefixes = set()
    with util.read_csv(upasargas) as reader:
        all_prefixes.update([x['name'] for x in reader])
    with util.read_csv(other) as reader:
        all_prefixes.update([x['name'] for x in reader])

    # The 's' prefix is used in roots like 'saMskf' and 'parizkf'. Although it
    # is prefixed to a verb, it is not semantically the same as the other verb
    # prefixes. Here, though, we treat it as a verb prefix.
    all_prefixes.add('s')

    # Some prefixes have alternate forms.
    prefix_alternates = {
        'pi': 'api',
        'ut': 'ud',
        'Ri': 'ni',
        'niz': 'nis',
        'iz': 'nis',
        'palA': 'parA',
        'pali': 'pari',
        'z': 's',
    }
    all_prefixes.update(prefix_alternates.keys())

    # Loading sandhi rules
    sandhi = make_sandhi_object(sandhi_rules)

    with util.read_csv(prefixed_roots) as reader:
        rows = []
        for row in reader:
            # Nibble away at `prefixed_root` until we have all prefixes for the
            # given root.
            prefixes = []
            prefixed_root = row['prefixed_root']
            unprefixed_root = row['unprefixed_root']
            last_letter = None

            q = Queue.PriorityQueue()
            for remainder in sandhi.split_off(prefixed_root, unprefixed_root):
                q.put_nowait((0, (), remainder))

            while not q.empty():
                _, cur_prefixes, remainder = q.get_nowait()

                # `remainder` is something we recognize: we're done!
                if remainder in all_prefixes:
                    prefixes = list(cur_prefixes)
                    if remainder:
                        prefixes.append(remainder)
                        last_letter = remainder[-1]
                    break

                for before, after in sandhi.splits(remainder):
                    # Prevent recursion. As of this comment, the `splits` method
                    # returns the non-split of some term X as (X, ''). In other
                    # words, this conditional will *never* be true. But since the
                    # behavior of various functions is still unsettled, this check
                    # will stay here for the time being.
                    if after == remainder:
                        continue

                    if before in all_prefixes:
                        state = (cur_prefixes + (before,), after)
                        cost = len(after)

                        # Incentivize short vowels. This avoids errors with roots
                        # like "upodgrah" ("upa-ud-grah"). Without the incentive,
                        # we could have "upa-A-ud-grah" instead.
                        if before and before[-1] in 'aiufx':
                            cost -= 1
                        q.put_nowait((cost,) + state)

            # Convert 'alternate' prefixes back to their original forms.
            prefixes = [prefix_alternates.get(x, x) for x in prefixes]
            if not prefixes:
                # Occurs if the root's prefix is unrecognized
                continue

            # We still don't know the prefix group. We can find it by splitting
            # off the root and keeping whatever matches `last_letter`.
            for group in sandhi.split_off(prefixed_root, unprefixed_root):
                if group[-1] == last_letter:
                    break
            prefix_string = '-'.join(prefixes)
            rows.append((group, prefix_string))

    labels = ['group', 'prefixes']
    with util.write_csv(out_path, labels) as write_row:
        for row in util.unique(rows):
            datum = dict(zip(labels, row))
            write_row(datum)


def write_mw_prefixed_roots(prefixed_roots, unprefixed_roots, prefix_groups,
                            sandhi_rules, out_path):
    """Parse the prefixes in a prefix root and write the parsed roots."""

    with util.read_csv(prefix_groups) as reader:
        prefix_groups = {x['group']: x['prefixes'] for x in reader}

    sandhi = make_sandhi_object(sandhi_rules)

    with util.read_csv(prefixed_roots) as reader:
        rows = []
        for row in reader:
            for group in sandhi.split_off(row['prefixed_root'],
                                          row['unprefixed_root']):
                if group in prefix_groups:
                    rows.append((row['prefixed_root'], prefix_groups[group],
                                 row['unprefixed_root'], row['hom']))
                    break

    labels = ['prefixed_root', 'prefixes', 'unprefixed_root', 'hom']
    with util.write_csv(out_path, labels) as write_row:
        for row in rows:
            write_row(dict(zip(labels, row)))


def get_mw_root_from_shs_root(root, blacklist, override):
    if root in blacklist:
        return None

    if root in override:
        return override[root]

    return root.partition('#')[0]


def write_shs_verbal_data(data_path, blacklist_path, override_path, out_path):
    """Write Sanskrit Heritage Site data after converting its roots.

    :param data_path: path to the actual verb data
    :param blacklist_path: path to a list of blacklisted roots
    :param override_path: path to a map from SHS roots to MW roots. If a root
                          isn't in this map, assume the SHS roots are just fine.
    :param out_path:
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

    with util.write_csv(out_path, labels) as write_row:
        for row in clean_rows:
            write_row(row)


def write_shs_verbal_indeclinables(adverbs_path, final_path, blacklist_path,
                                   override_path, out_path):
    """Write SHS verbal indeclinables."""
    with util.read_csv(blacklist_path) as reader:
        blacklist = {x['name'] for x in reader}

    with util.read_csv(override_path) as reader:
        override = {x['shs']: x['mw'] for x in reader}

    labels = None
    clean_rows = []
    with util.read_csv(adverbs_path) as reader:
        for row in reader:
            root = get_mw_root_from_shs_root(row['root'], blacklist=blacklist,
                                             override=override)
            if root is None:
                continue
            row['root'] = root
            clean_rows.append(row)

        labels = reader.fieldnames

    with util.read_csv(final_path) as reader:
        for row in reader:
            root = get_mw_root_from_shs_root(row['root'], blacklist=blacklist,
                                             override=override)
            if root is None:
                continue

            # TODO: handle 'ya' gerunds
            if not row['form'].endswith('um'):
                continue

            row['root'] = root
            clean_rows.append(row)

        assert labels == reader.fieldnames

    with util.write_csv(out_path, labels) as write_row:
        for row in clean_rows:
            write_row(row)

# ------------------
# Prefixed verb data
# ------------------


def write_prefixed_shs_verbal_data(data_path, prefixed_roots, blacklist_path,
                                   override_path, sandhi_rules, out_path):
    """Write Sanskrit Heritage Site data after converting its roots.

    :param data_path: path to the actual verb data
    :param blacklist_path: path to a list of blacklisted roots
    :param override_path: path to a map from SHS roots to MW roots. If a root
                          isn't in this map, assume the SHS roots are just fine.
    :param out_path:
    """
    with util.read_csv(blacklist_path) as reader:
        blacklist = {x['name'] for x in reader}

    with util.read_csv(override_path) as reader:
        override = {x['shs']: x['mw'] for x in reader}

    sandhi = make_sandhi_object(sandhi_rules)

    root_to_prefixed = {}
    with util.read_csv(prefixed_roots) as reader:
        for row in reader:
            root_to_prefixed.setdefault(row['unprefixed_root'], []).append(row)

    labels = None
    clean_rows = []
    with util.read_csv(data_path) as reader:
        for row in reader:
            root = get_mw_root_from_shs_root(row['root'], blacklist=blacklist,
                                             override=override)
            if root is None:
                continue
            row['root'] = root

            for result in root_to_prefixed.get(root, []):
                new_row = row.copy()
                for field in ['form', 'stem']:
                    if field in row:
                        new_row[field] = sandhi.join(
                            result['prefixes'].split('-') + [new_row[field]])
                new_row['root'] = result['prefixed_root']
                new_row['hom'] = result['hom']
                clean_rows.append(new_row)
        labels = reader.fieldnames + ['hom']

    with util.write_csv(out_path, labels) as write_row:
        for row in clean_rows:
            write_row(row)


def write_prefixed_shs_verbal_indeclinables(adverbs_path, final_path,
            sandhi_rules,
            prefixed_roots, blacklist_path, override_path, out_path):
    """Write prefixed SHS verbal indeclinables."""
    with util.read_csv(blacklist_path) as reader:
        blacklist = {x['name'] for x in reader}

    with util.read_csv(override_path) as reader:
        override = {x['shs']: x['mw'] for x in reader}

    sandhi = make_sandhi_object(sandhi_rules)

    root_to_prefixed = {}
    with util.read_csv(prefixed_roots) as reader:
        for row in reader:
            root_to_prefixed.setdefault(row['unprefixed_root'], []).append(row)

    labels = None
    clean_rows = []
    with util.read_csv(adverbs_path) as reader:
        for row in reader:
            root = get_mw_root_from_shs_root(row['root'], blacklist=blacklist,
                                             override=override)
            if root is None:
                continue
            row['root'] = root

            for result in root_to_prefixed.get(root, []):
                new_row = row.copy()
                for field in ['form', 'stem']:
                    if field in row:
                        new_row[field] = sandhi.join(
                            result['prefixes'].split('-') + [new_row[field]])
                new_row['root'] = result['prefixed-root']
                new_row['hom'] = result['hom']
                clean_rows.append(new_row)

        labels = reader.fieldnames

    with util.read_csv(final_path) as reader:
        for row in reader:
            root = get_mw_root_from_shs_root(row['root'], blacklist=blacklist,
                                             override=override)
            if root is None:
                continue

            # TODO: handle 'ya' gerunds
            if not row['form'].endswith('um'):
                continue

            row['root'] = root

            for result in root_to_prefixed.get(root, []):
                new_row = row.copy()
                for field in ['form', 'stem']:
                    if field in row:
                        new_row[field] = sandhi.join(
                            result['prefixes'].split('-') + [new_row[field]])
                new_row['root'] = result['prefixed-root']
                new_row['hom'] = result['hom']
                clean_rows.append(new_row)

        assert labels == reader.fieldnames

    labels += ['hom']
    with util.write_csv(out_path, labels) as write_row:
        for row in clean_rows:
            write_row(row)


def build_data(make_prefixed_verbals):
    paths = make_path_map(
        [('mw', 'monier-williams'),
         ('shs', 'sanskrit-heritage-site'),
         ('lso', 'learnsanskrit.org')])

    def heading(s):
        print '# ' + s + '...'

    heading('Nouns, pronouns, and adjectives')
    # TODO: irregular nominals
    copy_to_output_dir(paths['mw/nominals'], get_output_path('nominals.csv'))
    copy_to_output_dir(paths['lso/pronouns-inflected'],
                       get_output_path('pronouns.csv'))

    heading('Simple indeclinables')
    copy_to_output_dir(paths['mw/indeclinables'],
                       get_output_path('indeclinables.csv'))

    heading('Verb prefixes')
    write_verb_prefixes(upasargas=paths['lso/upasargas'],
                        other=paths['mw/verb-prefixes'],
                        out_path=get_output_path('verb-prefixes.csv'))

    heading('Prefix groups')
    write_prefix_groups(paths['mw/prefixed-roots'],
                        unprefixed_roots=paths['mw/unprefixed-roots'],
                        upasargas=paths['lso/upasargas'],
                        other=paths['mw/verb-prefixes'],
                        sandhi_rules=paths['lso/sandhi-rules'],
                        out_path=get_output_path('prefix-groups.csv'))

    heading('Roots')
    # NOTE: prefixed roots depend on output from write_prefix_groups
    copy_to_output_dir(paths['mw/unprefixed-roots'], 'unprefixed-roots.csv')
    write_mw_prefixed_roots(paths['mw/prefixed-roots'],
                            unprefixed_roots=paths['mw/unprefixed-roots'],
                            prefix_groups=get_output_path('prefix-groups.csv'),
                            sandhi_rules=paths['lso/sandhi-rules'],
                            out_path=get_output_path('prefixed-roots.csv'))

    heading('Verbs')
    write_shs_verbal_data(data_path=paths['shs/roots'],
                          override_path=paths['shs/root-override'],
                          blacklist_path=paths['shs/root-blacklist'],
                          out_path=get_output_path('verbs.csv'))

    heading('Participles')
    write_shs_verbal_data(data_path=paths['shs/parts'],
                          override_path=paths['shs/root-override'],
                          blacklist_path=paths['shs/root-blacklist'],
                          out_path=get_output_path('participles.csv'))

    heading('Verbal indeclinables')
    write_shs_verbal_indeclinables(adverbs_path=paths['shs/adverbs'],
                   final_path=paths['shs/final'],
                   override_path=paths['shs/root-override'],
                   blacklist_path=paths['shs/root-blacklist'],
                   out_path=get_output_path('verbal-indeclinables.csv'))

    # Sandhi rules
    copy_to_output_dir(paths['lso/sandhi-rules'], 'sandhi-rules.csv')

    if make_prefixed_verbals:
        heading('Prefixed verbs')
        write_prefixed_shs_verbal_data(data_path=paths['shs/roots'],
                   prefixed_roots=get_output_path('prefixed-roots.csv'),
                   override_path=paths['shs/root-override'],
                   blacklist_path=paths['shs/root-blacklist'],
                   sandhi_rules=paths['lso/sandhi-rules'],
                   out_path=get_output_path('prefixed-verbs.csv'))

        heading('Prefixed participles')
        write_prefixed_shs_verbal_data(data_path=paths['shs/parts'],
                   prefixed_roots=get_output_path('prefixed-roots.csv'),
                   override_path=paths['shs/root-override'],
                   blacklist_path=paths['shs/root-blacklist'],
                   sandhi_rules=paths['lso/sandhi-rules'],
                   out_path=get_output_path('prefixed-participles.csv'))

        heading('Prefixed indeclinables')
        write_prefixed_shs_verbal_indeclinables(
            adverbs_path=paths['shs/adverbs'],
            final_path=paths['shs/final'],
            prefixed_roots=get_output_path('prefixed-roots.csv'),
            override_path=paths['shs/root-override'],
            blacklist_path=paths['shs/root-blacklist'],
            sandhi_rules=paths['lso/sandhi-rules'],
            out_path=get_output_path('prefixed-verbal-indeclinables.csv'))


def main():
    args = parser.parse_args()
    build_data(make_prefixed_verbals=args.make_prefixed_verbals)


if __name__ == '__main__':
    main()
