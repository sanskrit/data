import os
import re

import pytest


PROJECT_DIR = os.path.dirname(__file__)
MW_DIR = os.path.join(PROJECT_DIR, 'monier-williams')
SHS_DIR = os.path.join(PROJECT_DIR, 'sanskrit-heritage-site')
LSO_DIR = os.path.join(PROJECT_DIR, 'learnsanskrit.org')


def iter_csv_paths(dirs):
    for d in dirs:
        for filename in os.listdir(d):
            if filename.endswith('.csv'):
                yield os.path.join(d, filename)


def test_consistent_column_names():
    """Checks that all CSV column names are unique and well-formed."""
    for path in iter_csv_paths([MW_DIR, SHS_DIR, LSO_DIR]):
        with open(path, 'r') as f:
            first_line = f.readline()
            column_names = first_line.strip().split(',')
            for c in column_names:
                # 'L' is for greeklist.csv
                assert re.match('^[a-z_L]+$', c), (filename, c)
            assert len(set(column_names)) == len(column_names), column_names


@pytest.mark.parametrize('path', list(iter_csv_paths([MW_DIR])))
def test_consistent_mw_data(path):
    """Checks that all CSV data is well-typed."""

    STEM_RE = r'([a-zA-Z\|]+|_)'
    types = {
        # TODO: '?', 'S1', '%26'
        'betacode': r'([A-Z ()=/\-*+\'%0-9]+|\?|S1)',
        'index': '[0-9]',
        'L': '[0-9\.]+',

        # Nominals
        'stem': STEM_RE,
        'stem_genders': '([mfn]+|none)',

        # Prefixes and indeclinables
        'name': STEM_RE,
        'prefix_type': '(upasarga|cvi|DAc|other)',

        # Roots
        'class': r'(1|2|3|4|5|6|7|8|9|10|denom)',
        'hom': r'[0-9]?',
        'prefixed_root': STEM_RE,
        'root': STEM_RE,
        'unprefixed_root': STEM_RE,
        'voice': '(para|atma)',
    }

    with open(path, 'r') as f:
        first = True
        regex = None
        for line in f:
            if first:
                column_names = line.strip().split(',')
                for c in column_names:
                    assert c in types, "Untyped column %s" % c
                regex_body = ','.join(types[c] for c in column_names)
                regex = '^' + regex_body + '$'
                first = False
                continue

            line = line.strip()
            assert re.match(regex, line), (regex, line)


@pytest.mark.parametrize('path', list(iter_csv_paths([SHS_DIR])))
def test_consistent_shs_data(path):
    """Checks that all CSV data is well-typed."""

    STEM_RE = r'([a-zA-Z\|]+|_)'
    ROOT_RE = '[a-zA-Z]+(#[1-9])?'
    types = {
        'betacode': '[A-Z()/]+',
        'index': '[0-9]',
        'L': '[0-9]+',

        'case': r'[12345678]',
        'class': r'(1|2|3|4|5|6|7|8|9|10|denom|)',
        'form': STEM_RE,
        'form_gender': '[mfn]',
        'pos': '(gerund|infinitive)',
        'root': ROOT_RE,
        'name': ROOT_RE,
        'shs': ROOT_RE,
        'mw': r'[a-zA-Z]+',
        'stem': STEM_RE,
        'stem_genders': '([mfn]+|none)',

        'person': '[123]',
        'number': r'[sdp]',
        'mode': r'(pres|impv|past|ipft|opt|ben|inj|perf|fut|sfut|pfut|cond|aor)',
        'modification': r'(|caus|denom|desid|intens)',
        'voice': '(para|atma|pass|active)',
    }

    with open(path, 'r') as f:
        first = True
        regex = None
        for line in f:
            if first:
                column_names = line.strip().split(',')
                for c in column_names:
                    assert c in types, "Untyped column %s" % c
                regex_body = ','.join(types[c] for c in column_names)
                regex = '^' + regex_body + '$'
                first = False
                continue

            line = line.strip()
            assert re.match(regex, line), (regex, line)


@pytest.mark.parametrize('path', list(iter_csv_paths([LSO_DIR])))
def test_consistent_lso_data(path):
    """Checks that all CSV data is well-typed."""

    STEM_RE = r'([a-zA-Z]+|_)'
    types = {
        # Upasargas
        'name': STEM_RE,

        # Nominals and nominal endings
        'ending': r'([a-zA-Z]+|)',
        'case': r'[12345678]',
        'form': STEM_RE,
        'number': r'[sdp]',
        'stem': STEM_RE,
        'stem_genders': '([mfn]+|none)',
        'form_gender': '([mfn]|none)',

        # Verb endings
        'category': '(both|simple|complex)',
        'person': '[123]',
        'number': '[sdp]',
        'mode': r'(pres|impv|past|ipft|opt|ben|inj|perf|fut|sfut|dfut|cond|aor)',
        'voice': '(para|atma)',

        # Sandhi
        'first': '[a-zA-Z]+',
        'second': '[a-zA-Z]*',
        'result': '[a-zA-Z ~\']+',
        'type': '(common|internal|external)'
    }

    with open(path, 'r') as f:
        first = True
        regex = None
        for line in f:
            if first:
                column_names = line.strip().split(',')
                for c in column_names:
                    assert c in types, "Untyped column %s" % c
                regex_body = ','.join(types[c] for c in column_names)
                regex = '^' + regex_body + '$'
                first = False
                continue

            line = line.strip()
            assert re.match(regex, line), (regex, line)
