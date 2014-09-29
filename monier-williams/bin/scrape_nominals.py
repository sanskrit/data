import re
import sys
import xml.etree.cElementTree as ET

import util


def scrape(xml_path):
    """Scrape nouns and adjectives from the MW dictionary."""

    noun_lexes = {
        'm': 'm',
        'f': 'f',
        'n': 'n',
        'mf': 'mf',
        'fn': 'fn',
        'nf': 'fn',
        'mn': 'mn',
        'nm': 'mn'
    }
    adj_lexes = {
        'mfn': 'mfn'
    }
    labels = ['stem', 'stem_genders']
    regexp = '(<lex>[^i].*?</lex>)'

    rows = []
    seen = set()
    for i, xml in enumerate(util.iter_mw_xml(xml_path, regexp=regexp)):
        # Genders
        lex = xml.find('body/lex')
        if lex is None:
            lex = xml.find('body/p/lex')
            if lex is None:
                continue
        lex.tag = None
        lex.tail = None
        lex = ET.tostring(lex)
        lex = re.sub('<.*>', '', lex)
        lex = re.sub('[^a-z]', '', lex)
        if lex not in noun_lexes and lex not in adj_lexes:
            continue
        genders = noun_lexes.get(lex) or adj_lexes.get(lex)
        assert genders

        # Stem
        stem = xml.find('h/key1').text

        if (stem, genders) in seen:
            continue
        seen.add((stem, genders))

        rows.append((stem, genders))

    rows.sort(key=lambda x: util.key_fn(x[0]))
    print util.make_csv_string(labels, rows)


def main():
    path = sys.argv[1]
    scrape(path)


if __name__ == '__main__':
    main()
